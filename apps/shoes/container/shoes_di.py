from typing import Text, Any
from injector import Module, Binder
from shared.domain.bus.query_bus import QueryBus
from shared.domain.bus.command_bus import CommandBus


class ShoesDi(Module):

    @staticmethod
    def __register_shoes_queries(bus: QueryBus) -> None:
        pass

    @staticmethod
    def __register_shoes_commands(bus: CommandBus) -> None:
        pass

    def configure(self, binder: Binder) -> None:
        pass
