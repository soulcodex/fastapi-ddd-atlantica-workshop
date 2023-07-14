import aiomysql
from aiologger import Logger
from aiomysql import Connection
from abc import ABC, abstractmethod
from pypika import MySQLQuery, Table
from shared.domain.types.aggregate_root import AggregateRoot
import shared.infrastructure.mysql.async_connection_pool as mysql
from typing import Text, AsyncIterator, Callable, Coroutine, Any, List


class MysqlAsyncRepository(ABC):

    def __init__(self, table_name: Text, connection: mysql.AsyncConnectionPool, logger: Logger):
        self.table_name = table_name
        self._connection = connection
        self._logger = logger

    async def query_builder(self) -> Table:
        return MySQLQuery.Table(self.table_name)

    @abstractmethod
    async def fields_list(self, aggregate: AggregateRoot) -> List[Any]:
        pass

    async def _transaction(self, tx: Callable[..., Coroutine[Any, Any, Any]]) -> None:
        try:
            async with self._connection.writer.cursor() as cursor:
                await cursor.execute('START TRANSACTION;')
                await tx()
                await cursor.execute('COMMIT;')
        except aiomysql.Error:
            self._logger.warning('Transaction failure... [ROLLBACK]')
            await cursor.execute('ROLLBACK;')
