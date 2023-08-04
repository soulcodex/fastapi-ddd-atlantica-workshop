import aiomysql
import databases
from fastapi import Depends
from aiologger import Logger
from typing_extensions import Annotated
from typing import AsyncIterator, Type, cast
from shoes.domain.shoe import ShoesRepository
from shared.domain.bus.query_bus import QueryBus
from shared.domain.bus.command_bus import CommandBus
from shared.domain.types import time_provider, domain_event
from shoes.domain.types import ShoesQueryBus, ShoesCommandBus
from shoes.application.create_shoe import CreateShoeCommand, CreateShoeCommandHandler
from shoes.application.find_shoe_by_id import FindShoeByIdQuery, FindShoeByIdQueryHandler
from shoes.infrastructure.persistence.mysql_shoes_repository import MysqlShoesRepository

from apps.shoes.dependency_injection.common import \
    configure_database_connection_pool, \
    configure_logger, \
    configure_query_bus, \
    configure_command_bus, \
    configure_event_publisher, \
    configure_time_provider


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


async def configure_create_shoe_command_handler(
        repository: Annotated[ShoesRepository, Depends(shoes_repository)],
        publisher: Annotated[domain_event.DomainEventPublisher, Depends(configure_event_publisher)],
        t_provider: Annotated[time_provider.TimeProvider, Depends(configure_time_provider)]
) -> CreateShoeCommandHandler:
    return CreateShoeCommandHandler(
        repository=repository,
        publisher=publisher,
        time_provider=t_provider
    )


async def shoes_command_bus(
        create_shoe_command_handler: Annotated[
            CreateShoeCommandHandler,
            Depends(configure_create_shoe_command_handler, use_cache=False)
        ],
        bus: Annotated[CommandBus, Depends(configure_command_bus)]
) -> ShoesCommandBus:
    await bus.register_command(CreateShoeCommand, create_shoe_command_handler)
    return cast(configure_command_bus, bus)
