from typing import Optional
from aiomysql import Connection, DictCursor


class AsyncConnectionPool:

    def __init__(self, writer: Connection, reader: Optional[Connection] = None):
        self.writer = writer
        if reader is None:
            writer.cursorclass = DictCursor
            self.reader = writer
            return
        self.reader = reader

    @classmethod
    async def only_writer(cls, writer: Connection) -> 'AsyncConnectionPool':
        return AsyncConnectionPool(writer=writer)

    async def close(self) -> None:
        await self.writer.close()
        if self.reader is not None:
            await self.reader.close()
