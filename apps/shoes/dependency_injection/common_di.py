import pyxdi
from aiologger import Logger
from typing import AsyncIterator
from shared.domain.bus import query_bus, command_bus
from shared.domain import environment_handler as environment
from shared.domain.types import identifier_provider, time_provider

import shared.infrastructure.mysql.async_connection_pool as mysql
import shared.infrastructure.mysql.async_helpers as mysql_helpers
import shared.infrastructure.identifier_providers as id_providers
import shared.infrastructure.time_providers as time_providers


class CommonDi(pyxdi.Module):

    @pyxdi.provider(scope='request')
    async def configure_logger(self) -> Logger:
        return Logger.with_default_handlers(name='shoes-api-logger')

    @pyxdi.provider(scope='request')
    async def configure_environment_handler(self) -> AsyncIterator[environment.EnvironmentHandler]:
        yield environment.NativeEnvironmentHandler()

    @pyxdi.provider(scope='request')
    async def configure_query_bus(self, logger: Logger) -> AsyncIterator[query_bus.QueryBus]:
        yield query_bus.AwaitableQueryBus(logger=logger)

    @pyxdi.provider(scope='request')
    async def configure_command_bus(self, logger: Logger) -> AsyncIterator[command_bus.CommandBus]:
        yield command_bus.AwaitableCommandBus(logger=logger)

    @pyxdi.provider(scope='request')
    async def configure_mysql_connection_pool(
            self,
            env: environment.EnvironmentHandler
    ) -> AsyncIterator[mysql.AsyncConnectionPool]:
        host, user, password, port, database = (
            env.get_value('MYSQL_WRITER_HOST'),
            env.get_value('MYSQL_WRITER_USER'),
            env.get_value('MYSQL_WRITER_PASSWORD'),
            env.get_value('MYSQL_WRITER_PORT'),
            env.get_value('MYSQL_DATABASE')
        )
        writer = await mysql_helpers.create_mysql_writer(user, password, host, port, database)
        yield await mysql.AsyncConnectionPool.only_writer(writer)
        writer.close()

    @pyxdi.provider(scope='request')
    async def configure_uuid_provider(self) -> AsyncIterator[identifier_provider.UuidProvider]:
        yield id_providers.RandomUuidProvider()

    @pyxdi.provider(scope='request')
    async def configure_ulid_provider(self) -> AsyncIterator[identifier_provider.UlidProvider]:
        yield id_providers.RandomUlidProvider()

    @pyxdi.provider(scope='request')
    async def configure_time_provider(self) -> AsyncIterator[time_provider.TimeProvider]:
        yield time_providers.SystemTimeProvider()
