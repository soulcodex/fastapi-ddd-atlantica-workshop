import shared.domain.bus.query_bus as query_bus
import shared.domain.bus.command_bus as command_bus
import shared.infrastructure.mysql.async_connection_pool as mysql
import shared.infrastructure.mysql.async_helpers as mysql_helpers

from typing import Callable, Coroutine, Any
from shared.domain import environment_handler
from logging import Logger, config as logger_config
from injector import Module, Binder, singleton, provider


class CommonDi(Module):
    @provider
    def provide_logger(self) -> Logger:
        logger_config.fileConfig(fname='./container/config/logging.ini')
        return Logger(name='shoes-api-logger')

    @provider
    def mysql_connection_pool(
            self,
            env: environment_handler.EnvironmentHandler
    ) -> Callable[[], Coroutine[Any, Any, mysql.AsyncConnectionPool]]:
        async def generate_mysql_connection_pool() -> mysql.AsyncConnectionPool:
            host, user, password, port, database = (
                env.get_value("MYSQL_WRITER_HOST"),
                env.get_value("MYSQL_WRITER_USER"),
                env.get_value("MYSQL_WRITER_PASSWORD"),
                env.get_value("MYSQL_WRITER_PORT"),
                env.get_value("MYSQL_DATABASE"),
            )
            writer = await mysql_helpers.create_async_writer(user, password, host, int(port), database)
            return mysql.AsyncConnectionPool.only_writer(writer=writer)
        return generate_mysql_connection_pool

    @singleton
    @provider
    def provide_environment_handler(self) -> environment_handler.EnvironmentHandler:
        env_handler = environment_handler.NativeEnvironmentHandler()
        self.__injector__.binder.bind(environment_handler.EnvironmentHandler, env_handler)
        return env_handler

    @singleton
    @provider
    def provide_query_bus(self, logger: Logger) -> query_bus.QueryBus:
        bus = query_bus.AwaitableQueryBus(logger=logger)
        self.__injector__.binder.bind(query_bus.QueryBus, bus)
        return bus

    @singleton
    @provider
    def provide_command_bus(self, logger: Logger) -> command_bus.CommandBus:
        bus = command_bus.AwaitableCommandBus(logger=logger)
        self.__injector__.binder.bind(command_bus.CommandBus, bus)
        return bus
