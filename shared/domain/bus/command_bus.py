from logging import Logger
from abc import ABC, abstractmethod
from shared.domain.bus.dto import Dto
from typing import Any, Dict, Text, Callable, Awaitable, Coroutine, Type


class CommandHandler(ABC):

    @abstractmethod
    def handle(self, query: Type[Dto]) -> None:
        pass


class CommandBus(ABC):
    @abstractmethod
    def register_command(self, command: Type[Dto], handler: CommandHandler) -> None:
        pass

    @abstractmethod
    def get_command_handler(self, command: Type[Dto]) -> CommandHandler:
        pass

    @abstractmethod
    def dispatch(self, command: Dto) -> None:
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

    async def get_command_handler(self, command: Type[Dto]) -> CommandHandler:
        command_name = command.id()
        if command_name in self.handlers:
            return self.handlers[command_name]

        raise Exception('Command not registered', command_name)

    async def dispatch(self, command: Type[Dto]) -> None:
        handler = await self.get_command_handler(command)
        await handler.handle(command)
