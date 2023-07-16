from logging import Logger
from abc import ABC, abstractmethod
from shared.domain.bus.dto import Dto
from typing import Dict, Any, Text, Awaitable, Coroutine, Callable, Type


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


class AwaitableQueryBus(QueryBus):

    def __init__(self, logger: Logger):
        self.logger = logger
        self.handlers: Dict[Text, QueryHandler] = dict()

    async def register_query(self, query: Type[Dto], handler: QueryHandler) -> None:
        query_name = query.id()

        if query_name in self.handlers:
            raise Exception('Query already registered', query_name)

        self.handlers[query_name] = handler

    async def ask(self, query: Dto) -> Any:
        query_name = query.id()

        if query_name in self.handlers:
            return await self.handlers[query_name].handle(query)

        raise Exception('Query not registered', query_name)
