import pyxdi
from aiologger import Logger
from typing import AsyncIterator, Type

from shoes.domain.types import ShoesQueryBus
from shoes.domain.shoe import ShoesRepository
from shared.domain.bus.query_bus import QueryBus
import shared.infrastructure.mysql.async_connection_pool as mysql
from shoes.application.find_shoe_by_id import FindShoeByIdQuery, FindShoeByIdQueryHandler
from shoes.infrastructure.persistence.mysql_shoes_repository import MysqlShoesRepository


class ShoesDi(pyxdi.Module):

    @pyxdi.provider(scope='request')
    async def configure_shoes_repository(
            self,
            pool: mysql.AsyncConnectionPool,
            logger: Logger
    ) -> AsyncIterator[ShoesRepository]:
        yield MysqlShoesRepository('shoes', pool, logger)

    @pyxdi.provider(scope='request')
    async def register_shoes_queries(self, repo: ShoesRepository, qb: QueryBus) -> AsyncIterator[ShoesQueryBus]:
        await qb.register_query(FindShoeByIdQuery, FindShoeByIdQueryHandler(repository=repo))
        yield qb
