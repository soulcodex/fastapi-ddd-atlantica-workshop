import pytest
from pyxdi import PyxDI
from fastapi import FastAPI
from httpx import AsyncClient
from typing import AsyncIterator
from shoes.domain.shoe import ShoesRepository, Shoe
from shared.domain.types.identifier_provider import UlidProvider
from tests.support.pytest.identifer_fixtures import ulid_generator
from tests.shoes.infrastructure.pytest.shoe_pytest_factory import shoes_object_mother
from tests.support.pytest.fastapi_fixtures import fastapi_application as application, di_container


class TestFindShoeByIdAcceptance:

    @pytest.fixture
    async def shoe_factory(self, di_container, shoes_object_mother) -> AsyncIterator[Shoe]:
        repo = await di_container.aget_instance(ShoesRepository)
        shoe = shoes_object_mother.random_shoe()
        await repo.save(shoe)
        yield shoe

    async def test_find_one_shoe_by_id_success(self, application: FastAPI, shoe_factory) -> None:
        async with AsyncClient(app=application, base_url='http://testserver') as client:
            response = await client.get(f'/v1/shoes/{shoe_factory.id.value}')
            assert response.status_code == 200
            assert response.json() == {
                "id": shoe_factory.id.value,
                "available": shoe_factory.available.value,
                "color": shoe_factory.color.value,
                "name": shoe_factory.name.value,
                "price": shoe_factory.price.value_with_currency("€"),
                "size": shoe_factory.size.value
            }

    async def test_find_one_shoe_by_id_fails_because_shoe_doesnt_exists(
            self,
            application: FastAPI,
            ulid_generator: UlidProvider
    ) -> None:
        async with AsyncClient(app=application, base_url='http://testserver') as client:
            response = await client.get(f'/v1/shoes/{ulid_generator.generate().value}')
            assert response.status_code == 404
            assert response.json() == {"detail": "Shoe not exist."}

    async def test_find_one_shoe_by_id_fails_with_wrong_http_method(
            self,
            application: FastAPI,
            ulid_generator: UlidProvider
    ) -> None:
        async with AsyncClient(app=application, base_url='http://testserver') as client:
            response = await client.delete(f'/v1/shoes/{ulid_generator.generate().value}')
            assert response.status_code == 405
            assert response.json() == {"detail": "Method Not Allowed"}
