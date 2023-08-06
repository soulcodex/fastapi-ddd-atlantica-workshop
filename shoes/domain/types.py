from typing import NewType

from shared.domain.bus.command_bus import CommandBus
from shared.domain.bus.query_bus import QueryBus

ShoesQueryBus = NewType('ShoesQueryBus', QueryBus)
ShoesCommandBus = NewType('ShoesCommandBus', CommandBus)
