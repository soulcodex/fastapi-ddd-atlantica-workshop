import databases
import httpx
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI

from apps.shoes.dependency_injection import common, shoes
from apps.shoes.main import create_app
from shared.infrastructure import time_providers, identifier_providers
from shared.infrastructure.pytest import arrangers
from shoes.domain.shoe import ShoesRepository
from shoes.infrastructure.pytest.factory import ShoeObjectMother


@pytest_asyncio.fixture
async def application() -> FastAPI:
    app = create_app()
    app.dependency_overrides[common.configure_ulid_provider] = lambda: identifier_providers.FixedUlidProvider()
    app.dependency_overrides[common.configure_uuid_provider] = lambda: identifier_providers.FixedUuidProvider()
    app.dependency_overrides[common.configure_time_provider] = lambda: time_providers.FixedTimeProvider()

    return app


@pytest_asyncio.fixture
async def http_client(application: FastAPI) -> httpx.AsyncClient:
    async with LifespanManager(application):
        async with httpx.AsyncClient(app=application, base_url='http://testserver') as client:
            yield client
            await client.aclose()


@pytest_asyncio.fixture
async def shoes_factory() -> ShoeObjectMother:
    return ShoeObjectMother()


@pytest_asyncio.fixture
async def database_pool() -> databases.Database:
    env = await common.configure_environment_handler()
    pool = await common.configure_database_connection_pool(env=env)
    return pool


@pytest_asyncio.fixture
async def shoes_repository(database_pool: databases.Database) -> ShoesRepository:
    logger = await common.configure_logger()
    return await shoes.shoes_repository(database_pool, logger)


@pytest_asyncio.fixture
async def persistence_arranger(database_pool: databases.Database) -> arrangers.PersistenceArranger:
    return arrangers.MysqlPersistenceArranger(pool=database_pool, database='shoes_api')


@pytest_asyncio.fixture(autouse=True, scope='function')
async def setup_and_teardown(
        database_pool: databases.Database,
        persistence_arranger: arrangers.PersistenceArranger
):
    await database_pool.connect()
    await persistence_arranger.arrange()
    yield
    await database_pool.disconnect()
