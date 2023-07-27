import aiomysql
import databases
from fastapi import Depends
from aiologger import Logger
from typing_extensions import Annotated
from typing import AsyncIterator, Type, cast
from shoes.domain.types import ShoesQueryBus
from shoes.domain.shoe import ShoesRepository
from shared.domain.bus.query_bus import QueryBus
from shoes.application.find_shoe_by_id import FindShoeByIdQuery, FindShoeByIdQueryHandler
from shoes.infrastructure.persistence.mysql_shoes_repository import MysqlShoesRepository

from apps.shoes.dependency_injection.common import \
    configure_database_connection_pool, \
    configure_logger, \
    configure_query_bus


async def shoes_repository(
        pool: Annotated[databases.Database, Depends(configure_database_connection_pool)],
        logger: Annotated[Logger, Depends(configure_logger)]
) -> ShoesRepository:
    return MysqlShoesRepository(table_name='shoes', pool=pool, logger=logger)


async def shoes_query_bus(
        repo: Annotated[ShoesRepository, Depends(shoes_repository)],
        bus: Annotated[QueryBus, Depends(configure_query_bus)]
) -> ShoesQueryBus:
    await bus.register_query(FindShoeByIdQuery, FindShoeByIdQueryHandler(repository=repo))
    return cast(ShoesQueryBus, bus)
