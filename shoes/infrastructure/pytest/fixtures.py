import pytest
import aiomysql
import databases
import pytest_asyncio
from fastapi import FastAPI
from apps.shoes.main import create_app
from asgi_lifespan import LifespanManager
from contextlib import asynccontextmanager
from shoes.domain.shoe import ShoesRepository
from apps.shoes.dependency_injection import common, shoes
from shoes.infrastructure.pytest.factory import ShoeObjectMother
from shared.domain.types import time_provider, identifier_provider
from shared.infrastructure import time_providers, identifier_providers
from shared.infrastructure.pytest.arrangers import PersistenceArranger, MysqlPersistenceArranger


@pytest_asyncio.fixture
async def application() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_):
        yield

    app = create_app(lifespan=lifespan)
    app.dependency_overrides[common.configure_ulid_provider] = lambda _: identifier_providers.FixedUlidProvider()
    app.dependency_overrides[common.configure_uuid_provider] = lambda _: identifier_providers.FixedUuidProvider()
    app.dependency_overrides[common.configure_time_provider] = lambda _: time_providers.FixedTimeProvider()

    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture
async def shoes_factory() -> ShoeObjectMother:
    return ShoeObjectMother()


@pytest_asyncio.fixture
async def database_pool() -> databases.Database:
    env = await common.configure_environment_handler()
    return await common.configure_database_connection_pool(env=env)


@pytest_asyncio.fixture
async def shoes_repository(database_pool: databases.Database) -> ShoesRepository:
    logger = await common.configure_logger()
    return await shoes.shoes_repository(database_pool, logger)


@pytest_asyncio.fixture
async def database_arranger(database_pool: databases.Database) -> PersistenceArranger:
    env = await common.configure_environment_handler()
    return MysqlPersistenceArranger(pool=database_pool, database=env.get_value('MYSQL_DATABASE'))


@pytest_asyncio.fixture(autouse=True, scope="function")
async def before_after(database_arranger: PersistenceArranger, database_pool: databases.Database):
    await database_pool.connect()
    await database_arranger.arrange()
    yield
    await database_pool.disconnect()
