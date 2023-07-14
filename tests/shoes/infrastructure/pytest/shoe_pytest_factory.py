import pytest
from typing import AsyncIterator
from shoes.domain.shoe import ShoesRepository
from tests.shoes.domain.shoe import ShoeObjectMother


@pytest.fixture
async def shoes_object_mother() -> AsyncIterator[ShoeObjectMother]:
    yield ShoeObjectMother()
