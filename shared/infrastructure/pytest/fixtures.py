import pytest
from faker import Faker
from typing import AsyncIterator
from shared.domain.types.identifier_provider import UlidProvider, UuidProvider
from shared.infrastructure.identifier_providers import FixedUlidProvider, FixedUuidProvider


@pytest.fixture
async def faker() -> AsyncIterator[Faker]:
    faker_instance = Faker(['en-US', 'en_US', 'en_US', 'en-US'])
    yield faker_instance


@pytest.fixture
async def ulid_generator() -> AsyncIterator[UlidProvider]:
    yield FixedUlidProvider()


@pytest.fixture
async def uuid_generator() -> AsyncIterator[UlidProvider]:
    yield FixedUuidProvider()
