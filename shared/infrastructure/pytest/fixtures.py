import pytest
import asyncio
import aiomysql
from typing import AsyncIterator, Callable
from shared.domain.types.identifier_provider import UlidProvider, UuidProvider
from shared.infrastructure.identifier_providers import FixedUlidProvider, FixedUuidProvider
from shared.infrastructure.pytest.arrangers import PersistenceArranger, MysqlPersistenceArranger


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
