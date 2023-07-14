import pytest
from faker import Faker
from typing import AsyncIterator


@pytest.fixture
async def faker_() -> AsyncIterator[Faker]:
    faker_instance = Faker(['en-US', 'en_US', 'en_US', 'en-US'])
    yield faker_instance
