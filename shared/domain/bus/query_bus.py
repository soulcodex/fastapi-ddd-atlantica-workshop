from logging import Logger
from abc import ABC, abstractmethod
from shared.domain.bus.dto import Dto
from typing import Dict, Any, Text, Callable, Type


class QueryHandler(ABC):

    @abstractmethod
    async def handle(self, query: Dto) -> Any:
        pass


class QueryBus(ABC):
    @abstractmethod
    async def register_query(self, query: Type[Dto], handler: QueryHandler) -> None:
        pass

    @abstractmethod
    async def ask(self, query: Dto) -> Any:
        pass
