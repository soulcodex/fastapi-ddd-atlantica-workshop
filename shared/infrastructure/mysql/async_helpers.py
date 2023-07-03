import aiomysql
from typing import Text


async def dial_connection(user: Text, password: Text, host: Text, port: int, database: Text) -> None:
    con: aiomysql.Connection = aiomysql.connect(
        host=host,
        user=user,
        password=password,
        db=database,
        port=port
    )

    try:
        await con.ping()
    except e:
        raise Exception("Connection is closed") from e


async def create_async_reader(user: Text, password: Text, host: Text, port: int, database: Text) -> aiomysql.Connection:
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
    except e:
        raise Exception("Error creating async mysql reader") from e


async def create_async_writer(user: Text, password: Text, host: Text, port: int, database: Text) -> aiomysql.Connection:
    try:
        con: aiomysql.Connection = aiomysql.connect(
            host=host,
            user=user,
            password=password,
            db=database,
            port=port,
            autocommit=False,
            connect_timeout=180,
            cursorclass=aiomysql.DictCursor
        )

        await con.ping()

        return con
    except e:
        raise Exception("Error creating async mysql writer") from e
