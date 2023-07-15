import pytest
from pyxdi import PyxDI
from fastapi import FastAPI
from apps.shoes.main import app
from typing import AsyncIterator
from shoes.domain.shoe import ShoesRepository
from shoes.infrastructure.pytest.factory import ShoeObjectMother


@pytest.fixture
async def application() -> AsyncIterator[FastAPI]:
    yield app


@pytest.fixture
async def di_container() -> AsyncIterator[PyxDI]:
    container: PyxDI = app.state.di
    async with container.arequest_context():
        yield container
        await container.aclose()


@pytest.fixture
async def shoes_factory() -> AsyncIterator[ShoeObjectMother]:
    yield ShoeObjectMother()


@pytest.fixture
async def shoes_repository(di_container) -> AsyncIterator[ShoesRepository]:
    yield await di_container.aget_instance(ShoesRepository)
