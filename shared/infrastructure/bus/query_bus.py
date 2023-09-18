from logging import Logger
from typing import Dict, Text, Type, Any
from shared.domain.bus.dto import Dto, InvalidDto
from shared.domain.bus.query_bus import QueryBus, QueryHandler


class AwaitableQueryBus(QueryBus):

    def __init__(self, logger: Logger):
        self.logger = logger
        self.handlers: Dict[Text, QueryHandler] = dict()

    async def register_query(self, query: Type[Dto], handler: QueryHandler) -> None:
        query_name = query.id()

        if query_name in self.handlers:
            raise InvalidDto('Query <%s> already registered' % query_name)

        self.handlers[query_name] = handler

    async def ask(self, query: Dto) -> Any:
        query_name = query.id()

        if query_name in self.handlers:
            return await self.handlers[query_name].handle(query)

        raise InvalidDto('Query <%s> not registered' % query_name)
