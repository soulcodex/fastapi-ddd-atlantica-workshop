import aiomysql
import aio_pika
import aiologger
import databases
from logging import Logger
from fastapi import Depends
from typing_extensions import Annotated
from shared.domain.bus import query_bus, command_bus
from shared.domain import environment_handler as environment
from shared.domain.types import identifier_provider, time_provider

from shared.infrastructure.domain_event import rabbitmq_publisher, rabbitmq_helpers, json_event_serializer
import shared.infrastructure.mysql.async_helpers as mysql_helpers
import shared.infrastructure.identifier_providers as id_providers
import shared.infrastructure.time_providers as time_providers
import shared.infrastructure.pytest.arrangers as arrangers


async def configure_logger() -> Logger:
    return aiologger.Logger.with_default_handlers(name='shoes-api-logger')


async def configure_environment_handler() -> environment.EnvironmentHandler:
    return environment.NativeEnvironmentHandler()


async def configure_query_bus(
        logger: Annotated[Logger, Depends(configure_logger)]) -> query_bus.QueryBus:
    return query_bus.AwaitableQueryBus(logger=logger)


async def configure_command_bus(
        logger: Annotated[Logger, Depends(configure_logger)]) -> command_bus.CommandBus:
    return command_bus.AwaitableCommandBus(logger=logger)


async def configure_database_connection_pool(
        env: Annotated[environment.EnvironmentHandler, Depends(configure_environment_handler)]
) -> databases.Database:
    host, user, password, port, database = (
        env.get_value('MYSQL_WRITER_HOST'),
        env.get_value('MYSQL_WRITER_USER'),
        env.get_value('MYSQL_WRITER_PASSWORD'),
        env.get_value('MYSQL_WRITER_PORT'),
        env.get_value('MYSQL_DATABASE')
    )
    pool_generator = mysql_helpers.create_mysql_pool(user, password, host, port, database)
    async for pool in pool_generator:
        return pool


async def configure_event_publisher_connection(
        env: Annotated[environment.EnvironmentHandler, Depends(configure_environment_handler)]
) -> rabbitmq_publisher.RabbitMqEventPublisher:
    host, user, password, port, virtual_host, topic, service_name = (
        env.get_value('MESSAGE_BROKER_HOST'),
        env.get_value('MESSAGE_BROKER_USER'),
        env.get_value('MESSAGE_BROKER_PASSWORD'),
        env.get_value('MESSAGE_BROKER_PORT'),
        env.get_value('MESSAGE_BROKER_EVENTS_HOST'),
        env.get_value('MESSAGE_BROKER_EVENTS_TOPIC'),
        env.get_value('SERVICE_NAME')
    )
    rabbit_client = rabbitmq_helpers.create_rabbitmq_connection(user, password, host, port, virtual_host)
    async for client in rabbit_client:
        serializer = json_event_serializer.JsonDomainEventSerializer(service=service_name)
        return rabbitmq_publisher.RabbitMqEventPublisher(exchange=topic, client=client, serializer=serializer)


async def configure_database_arranger(
        pool: Annotated[databases.Database, Depends(configure_database_connection_pool)],
        env: Annotated[environment.EnvironmentHandler, Depends(configure_environment_handler)]
) -> arrangers.PersistenceArranger:
    return arrangers.MysqlPersistenceArranger(pool=pool, database=env.get_value('MYSQL_DATABASE'))


async def configure_uuid_provider() -> identifier_provider.UuidProvider:
    return id_providers.RandomUuidProvider()


async def configure_ulid_provider() -> identifier_provider.UlidProvider:
    return id_providers.RandomUlidProvider()


async def configure_time_provider() -> time_provider.TimeProvider:
    return time_providers.SystemTimeProvider()
