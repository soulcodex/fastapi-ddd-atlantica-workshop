from logging import Logger
from abc import ABC, abstractmethod
from shared.domain.bus.dto import Dto
from typing import Any, Dict, Text, Callable, Awaitable, Coroutine, Type


class CommandHandler(ABC):

    @abstractmethod
    async def handle(self, query: Dto) -> None:
        pass


class CommandBus(ABC):
    @abstractmethod
    async def register_command(self, command: Type[Dto], handler: CommandHandler) -> None:
        pass

    @abstractmethod
    async def dispatch(self, command: Dto) -> None:
        pass


class AwaitableCommandBus(CommandBus):

    def __init__(self, logger: Logger):
        self.logger = logger
        self.handlers: Dict[Text, CommandHandler] = dict()

    async def register_command(self, command: Type[Dto], handler: CommandHandler) -> None:
        command_name = command.id()

        if command_name in self.handlers:
            raise Exception('Command already registered', command_name)

        self.handlers[command_name] = handler

    async def dispatch(self, command: Dto) -> None:
        command_name = command.id()
        if command_name in self.handlers:
            return await self.handlers[command_name].handle(command)

        raise Exception('Command not registered', command_name)
