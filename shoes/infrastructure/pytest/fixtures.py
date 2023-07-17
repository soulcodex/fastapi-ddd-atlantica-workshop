import pytest
import pytest_asyncio
from pyxdi import PyxDI
from fastapi import FastAPI
from apps.shoes.main import app
from shoes.domain.shoe import ShoesRepository
from apps.shoes.dependency_injection import di
from pyxdi.core import RequestContext, ScopedContext
from shoes.infrastructure.pytest.factory import ShoeObjectMother
from typing import AsyncIterator, Callable, TypeVar, Type, Coroutine, Any

T = TypeVar('T')


@pytest_asyncio.fixture
async def application() -> FastAPI:
    return app


@pytest_asyncio.fixture
async def di_container() -> Callable[[Type[T]], T]:
    container: PyxDI = app.state.di

    # noinspection PyProtectedMember
    async def _dependency_resolver(dep: Type[T]) -> T:
        try:
            return await container.aget_instance(dep)
        except LookupError:
            container._request_context_var.set(RequestContext())
            return await container.aget_instance(dep)

    return _dependency_resolver


@pytest_asyncio.fixture
async def shoes_factory() -> ShoeObjectMother:
    return ShoeObjectMother()


@pytest_asyncio.fixture
async def shoes_repository(di_container) -> ShoesRepository:
    return di_container(ShoesRepository)


@pytest_asyncio.fixture(autouse=True)
async def before_after(di_container):
    pass
