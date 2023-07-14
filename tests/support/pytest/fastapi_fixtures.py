import pytest
from pyxdi import PyxDI
from fastapi import FastAPI
from apps.shoes.main import app
from typing import AsyncIterator
from apps.shoes.dependency_injection import di


@pytest.fixture
async def fastapi_application() -> AsyncIterator[FastAPI]:
    yield app


@pytest.fixture
async def di_container() -> AsyncIterator[PyxDI]:
    async with di.arequest_context():
        yield di
        await di.aclose()

