import shared.domain.bus.query_bus as query_bus
import shared.domain.bus.command_bus as command_bus

from logging import Logger, config as logger_config
from injector import Module, Binder, singleton, provider
from shared.domain.environment_handler import EnvironmentHandler, NativeEnvironmentHandler


class CommonDi(Module):
    @provider
    def provide_logger(self) -> Logger:
        logger_config.fileConfig(fname='./container/config/logging.ini')
        return Logger(name='shoes-api-logger')

    @singleton
    @provider
    def provide_environment_handler(self) -> EnvironmentHandler:
        return NativeEnvironmentHandler()

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
