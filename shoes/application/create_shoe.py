from typing import Text
from dataclasses import dataclass
from shared.domain.bus.dto import Dto
from shoes.domain.value_object import ShoeId
from shoes.domain.shoe import ShoesRepository, Shoe
from shared.domain.bus.command_bus import CommandHandler
from shared.domain.types.time_provider import TimeProvider
from shared.domain.types.domain_event import DomainEventPublisher


@dataclass
class CreateShoeCommand(Dto):
    shoe_id: Text
    name: Text
    color: Text
    size: int
    price: int
    available: bool

    @staticmethod
    def id() -> str:
        return "create_shoe_command"


class CreateShoeCommandHandler(CommandHandler):

    def __init__(self, repository: ShoesRepository, publisher: DomainEventPublisher, time_provider: TimeProvider):
        self._repository = repository
        self._publisher = publisher
        self._time_provider = time_provider

    async def handle(self, command: "CreateShoeCommand") -> None:
        now = self._time_provider.now()
        shoe = Shoe.create(
            command.shoe_id,
            command.name,
            command.color,
            command.size,
            command.price,
            command.available,
            now
        )
        events = shoe.pull_events()
        await self._repository.save(shoe)
        await self._publisher.publish(events)
