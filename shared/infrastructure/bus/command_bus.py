from logging import Logger
from typing import Type, Dict, Text
from shared.domain.bus.dto import Dto, InvalidDto
from shared.domain.bus.command_bus import CommandBus, CommandHandler


class AwaitableCommandBus(CommandBus):

    def __init__(self, logger: Logger):
        self.logger = logger
        self.handlers: Dict[Text, CommandHandler] = dict()

    async def register_command(self, command: Type[Dto], handler: CommandHandler) -> None:
        command_name = command.id()

        if command_name in self.handlers:
            raise InvalidDto('Command <%s> already registered' % command_name)

        self.handlers[command_name] = handler

    async def dispatch(self, command: Dto) -> None:
        command_name = command.id()
        if command_name in self.handlers:
            return await self.handlers[command_name].handle(command)

        raise InvalidDto('Command <%s> not registered' % command_name)
