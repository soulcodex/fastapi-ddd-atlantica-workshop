import pytest
import asyncio
import aiomysql
from faker import Faker
from typing import AsyncIterator, Callable
from shared.domain.types.identifier_provider import UlidProvider, UuidProvider
from shared.infrastructure.identifier_providers import FixedUlidProvider, FixedUuidProvider
from shared.infrastructure.pytest.arrangers import PersistenceArranger, MysqlPersistenceArranger


@pytest.fixture
async def faker() -> AsyncIterator[Faker]:
    faker_instance = Faker(['en-US', 'en_US', 'en_US', 'en-US'])
    yield faker_instance


@pytest.fixture
async def ulid_generator() -> UlidProvider:
    return FixedUlidProvider()


@pytest.fixture
async def uuid_generator() -> UuidProvider:
    return FixedUuidProvider()


@pytest.fixture
async def mysql_arranger() -> Callable[[aiomysql.Pool], PersistenceArranger]:
    def _arranger(pool: aiomysql.Pool) -> MysqlPersistenceArranger:
        return MysqlPersistenceArranger(pool=pool)

    return _arranger
