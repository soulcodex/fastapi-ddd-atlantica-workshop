import httpx
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
    app = create_app()
    app.dependency_overrides[common.configure_ulid_provider] = lambda _: identifier_providers.FixedUlidProvider()
    app.dependency_overrides[common.configure_uuid_provider] = lambda _: identifier_providers.FixedUuidProvider()
    app.dependency_overrides[common.configure_time_provider] = lambda _: time_providers.FixedTimeProvider()

    yield app


@pytest_asyncio.fixture
async def http_client(application: FastAPI) -> httpx.AsyncClient:
    async with LifespanManager(application):
        async with httpx.AsyncClient(app=application, base_url='http://testserver') as client:
            yield client


@pytest_asyncio.fixture
async def shoes_factory() -> ShoeObjectMother:
    return ShoeObjectMother()


@pytest_asyncio.fixture
async def database_pool() -> databases.Database:
    env = await common.configure_environment_handler()
    pool = await common.configure_database_connection_pool(env=env)
    await pool.connect()
    yield pool
    await pool.disconnect()


@pytest_asyncio.fixture
async def shoes_repository(database_pool: databases.Database) -> ShoesRepository:
    logger = await common.configure_logger()
    return await shoes.shoes_repository(database_pool, logger)
