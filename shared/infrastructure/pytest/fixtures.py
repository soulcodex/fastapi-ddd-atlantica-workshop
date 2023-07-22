import pytest
from shared.domain.types.identifier_provider import UlidProvider, UuidProvider
from shared.infrastructure.identifier_providers import FixedUlidProvider, FixedUuidProvider


@pytest.fixture
async def ulid_generator() -> UlidProvider:
    return FixedUlidProvider()


@pytest.fixture
async def uuid_generator() -> UuidProvider:
    return FixedUuidProvider()
