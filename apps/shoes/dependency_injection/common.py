import aiomysql
import aiologger
import databases
from logging import Logger
from fastapi import Depends
from typing_extensions import Annotated
from shared.domain.bus import query_bus, command_bus
from shared.domain import environment_handler as environment
from shared.domain.types import identifier_provider, time_provider

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


async def configure_mysql_connection_pool(
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


async def configure_database_arranger(
        pool: Annotated[databases.Database, Depends(configure_mysql_connection_pool)],
        env: Annotated[environment.EnvironmentHandler, Depends(configure_environment_handler)]
) -> arrangers.PersistenceArranger:
    return arrangers.MysqlPersistenceArranger(pool=pool, database=env.get_value('MYSQL_DATABASE'))


async def configure_uuid_provider() -> identifier_provider.UuidProvider:
    return id_providers.RandomUuidProvider()


async def configure_ulid_provider() -> identifier_provider.UlidProvider:
    return id_providers.RandomUlidProvider()


async def configure_time_provider() -> time_provider.TimeProvider:
    return time_providers.SystemTimeProvider()
