from typing import Type
from logging import Logger
from abc import ABC, abstractmethod
from shared.domain.bus.dto import Dto


class CommandHandler(ABC):

    @abstractmethod
    async def handle(self, command: Dto) -> None:
        pass


class CommandBus(ABC):
    @abstractmethod
    async def register_command(self, command: Type[Dto], handler: CommandHandler) -> None:
        pass

    @abstractmethod
    async def dispatch(self, command: Dto) -> None:
        pass
