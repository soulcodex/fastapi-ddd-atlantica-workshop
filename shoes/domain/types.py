from typing import NewType
from shared.domain.bus.query_bus import QueryBus
from shared.domain.bus.command_bus import CommandBus

ShoesQueryBus = NewType('ShoesQueryBus', QueryBus)
ShoesCommandBus = NewType('ShoesCommandBus', CommandBus)
