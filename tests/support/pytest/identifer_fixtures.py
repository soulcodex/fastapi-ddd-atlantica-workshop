import pytest
from typing import AsyncIterator
from tests.support.pytest.fastapi_fixtures import di_container
from shared.domain.types.identifier_provider import UlidProvider, UuidProvider


@pytest.fixture
async def ulid_generator(di_container) -> AsyncIterator[UlidProvider]:
    yield await di_container.aget_instance(UlidProvider)


@pytest.fixture
async def uuid_generator(di_container) -> AsyncIterator[UlidProvider]:
    yield await di_container.aget_instance(UuidProvider)
