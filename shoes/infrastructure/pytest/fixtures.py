import pytest
import asyncio
import aiomysql
import databases
import pytest_asyncio
from fastapi import FastAPI
from apps.shoes.main import app
from shoes.domain.shoe import ShoesRepository
from apps.shoes.dependency_injection import common, shoes
from shoes.infrastructure.pytest.factory import ShoeObjectMother
from shared.infrastructure.pytest.arrangers import PersistenceArranger, MysqlPersistenceArranger


@pytest_asyncio.fixture
async def application() -> FastAPI:
    return app


@pytest_asyncio.fixture
async def shoes_factory() -> ShoeObjectMother:
    return ShoeObjectMother()


@pytest_asyncio.fixture
async def database_pool() -> databases.Database:
    env = await common.configure_environment_handler()
    pool = await common.configure_mysql_connection_pool(env=env)
    return pool


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
