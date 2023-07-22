import aiomysql
import databases
from aiologger import Logger
from aiomysql import Connection
from abc import ABC, abstractmethod
from pypika import MySQLQuery, Table
from shared.domain.types.aggregate_root import AggregateRoot
from typing import Text, AsyncIterator, Callable, Coroutine, Any, List


class MysqlAsyncRepository(ABC):

    def __init__(self, table_name: Text, pool: databases.Database, logger: Logger):
        self.table_name = table_name
        self._pool = pool
        self._logger = logger

    async def query_builder(self) -> Table:
        return MySQLQuery.Table(self.table_name)

    @abstractmethod
    async def fields_values_list(self, aggregate: AggregateRoot) -> List[Any]:
        pass

    async def _transaction(self, tx: Callable[..., Coroutine[Any, Any, Any]]) -> None:
        transaction = await self._pool.transaction(force_rollback=True)
        try:
            await tx()
        except aiomysql.Error:
            await transaction.rollback()
            self._logger.warning('Transaction failure... [ROLLBACK]')
        else:
            await transaction.commit()
            self._logger.warning('Transaction commit... [COMMIT]')
