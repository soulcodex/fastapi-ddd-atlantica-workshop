import aiomysql
import databases
from typing import Text


def create_mysql_pool(
        user: Text,
        password: Text,
        host: Text,
        port: Text,
        database: Text
) -> databases.Database:
    return databases.Database(
        f'mysql+aiomysql://{user}:{password}@{host}:{port}/{database}',
        min_size=5,
        max_size=20,
    )
