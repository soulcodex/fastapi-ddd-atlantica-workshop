from typing import Text
from aiomysql import Connection
from abc import ABC, abstractmethod
import shared.infrastructure.mysql.async_connection_pool as mysql


class MysqlAsyncRepository(ABC):

    def __init__(self, table_name: Text, connection: mysql.AsyncConnectionPool):
        self.table_name = table_name
        self._connection = connection
