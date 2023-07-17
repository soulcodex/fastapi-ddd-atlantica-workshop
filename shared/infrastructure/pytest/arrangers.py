from typing import List, Text
from abc import ABC, abstractmethod
from shared.infrastructure.mysql.async_connection_pool import AsyncConnectionPool


class PersistenceArranger(ABC):

    @abstractmethod
    async def arrange(self) -> None:
        pass


class MysqlPersistenceArranger(PersistenceArranger):

    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool

    async def arrange(self) -> None:
        await self._list_tables()
        pass

    async def _list_tables(self) -> List[Text]:
        async with self.pool.writer.cursor() as cursor:
            query = 'SHOW TABLES'
            await cursor.execute(query)
            tables = await cursor.fetchmany()
            print(tables)
            return []
