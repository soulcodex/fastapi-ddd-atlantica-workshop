from typing import Text, Any
from shared.domain.bus.query_bus import QueryBus
from shared.domain.bus.command_bus import CommandBus
from injector import Module, Binder, singleton, provider
import shared.infrastructure.mysql.async_connection_pool as mysql

from shoes.domain.shoe import ShoeRepository
from shoes.infrastructure.persistence.mysql_shoes_repository import MysqlShoesRepository


class ShoesDi(Module):

    @singleton
    @provider
    def provide_mysql_shoe_repository(self, con: mysql.AsyncConnectionPool) -> ShoeRepository:
        return MysqlShoesRepository(table_name='shoes', connection=con)

    @staticmethod
    def __register_shoes_queries(bus: QueryBus) -> None:
        pass

    @staticmethod
    def __register_shoes_commands(bus: CommandBus) -> None:
        pass

    def configure(self, binder: Binder) -> None:
        pass
