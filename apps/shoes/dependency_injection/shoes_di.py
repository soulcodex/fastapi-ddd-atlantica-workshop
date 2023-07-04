import pyxdi
import shared.infrastructure.mysql.async_connection_pool as mysql

from shoes.domain.shoe import ShoeRepository
from typing import AsyncIterator, Type, NewType
from shared.domain.bus.query_bus import QueryBus
from shoes.application.find_shoe_by_id import FindShoeByIdQuery, FindShoeByIdQueryHandler
from shoes.infrastructure.persistence.mysql_shoes_repository import MysqlShoesRepository

ShoesQueryBus = NewType('ShoesQueryBus', QueryBus)


class ShoesDi(pyxdi.Module):

    @pyxdi.provider(scope='request')
    async def configure_shoes_repository(self, pool: mysql.AsyncConnectionPool) -> AsyncIterator[ShoeRepository]:
        yield MysqlShoesRepository('shoes', pool)

    @pyxdi.provider(scope='request')
    async def register_shoes_queries(self, repo: ShoeRepository, qb: QueryBus) -> AsyncIterator[ShoesQueryBus]:
        await qb.register_query(FindShoeByIdQuery, FindShoeByIdQueryHandler(repository=repo))
        yield qb
