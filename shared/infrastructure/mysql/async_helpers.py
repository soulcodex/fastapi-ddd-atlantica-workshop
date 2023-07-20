import aiomysql
import databases
from typing import Text, AsyncIterator


async def create_mysql_pool(
        user: Text,
        password: Text,
        host: Text,
        port: Text,
        database: Text
) -> AsyncIterator[databases.Database]:
    connection_string = f'mysql+aiomysql://{user}:{password}@{host}:{port}/{database}'
    con = databases.Database(
        connection_string,
        min_size=5,
        max_size=20,
    )
    await con.connect()
    yield con
    await con.disconnect()
