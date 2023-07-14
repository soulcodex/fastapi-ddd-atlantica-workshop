import aiomysql
from typing import Text


async def create_mysql_reader(user: Text, password: Text, host: Text, port: int, database: Text) -> aiomysql.Connection:
    try:
        con: aiomysql.Connection = aiomysql.connect(
            host=host,
            user=user,
            password=password,
            db=database,
            port=port,
            connect_timeout=180,
            cursorclass=aiomysql.DictCursor
        )

        await con.ping()

        return con
    except aiomysql.Error as e:
        raise Exception from e


async def create_mysql_writer(user: Text, password: Text, host: Text, port: Text, database: Text) -> aiomysql.Connection:
    try:
        con: aiomysql.Connection = await aiomysql.connect(
            host=host,
            user=user,
            password=password,
            db=database,
            port=int(port),
            autocommit=False,
            connect_timeout=180,
        )

        await con.ping()

        return con
    except aiomysql.Error as e:
        raise Exception from e
