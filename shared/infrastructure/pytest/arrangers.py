import aiomysql
import databases
from typing import List, Text
from abc import ABC, abstractmethod
from databases.interfaces import Record


class PersistenceArranger(ABC):

    @abstractmethod
    async def arrange(self) -> None:
        pass


class MysqlPersistenceArranger(PersistenceArranger):

    def __init__(self, pool: databases.Database, database: Text):
        self._pool = pool
        self._database = database
        self._ignore = ['migrations']

    async def arrange(self) -> None:
        tables = await self._list_tables()
        await self._truncate(tables)

    async def _truncate(self, tables: List[Text]) -> None:
        for table in tables:
            if table not in self._ignore:
                async with self._pool.connection() as conn:
                    query = f''' TRUNCATE TABLE {table} '''
                    await conn.execute(query=query)

    async def _list_tables(self) -> List[Text]:
        async with self._pool.connection() as conn:
            query = '''
                SELECT TABLE_NAME AS _tables 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = :database
            '''
            result = await conn.fetch_all(query=query, values={'database': self._database})
            tables = [table._mapping['_tables'] for _, table in enumerate(result)]
            return tables
