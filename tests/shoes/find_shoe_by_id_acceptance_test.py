import httpx
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from typing import AsyncIterator
from shoes.domain.shoe import ShoesRepository, Shoe
from shoes.infrastructure.pytest.fixtures import shoes_factory
from shared.domain.types.identifier_provider import UlidProvider
from shared.infrastructure.pytest.fixtures import ulid_generator
from shoes.infrastructure.pytest.fixtures import application, shoes_repository


class TestFindShoeByIdAcceptance:

    @pytest.fixture
    async def shoe_factory(self, shoes_repository, shoes_factory) -> Shoe:
        shoe = shoes_factory.random_shoe()
        await shoes_repository.save(shoe)
        return shoe

    @pytest.mark.asyncio
    async def test_find_one_shoe_by_id_success(self, http_client: httpx.AsyncClient, shoe_factory) -> None:
        shoe = await shoe_factory
        response = await http_client.get(f'/v1/shoes/{shoe.id.value}')
        assert response.status_code == 200
        assert response.json() == {
            "id": shoe.id.value,
            "available": shoe.available.value,
            "color": shoe.color.value,
            "name": shoe.name.value,
            "price": shoe.price.value_with_currency("€"),
            "size": shoe.size.value
        }

    @pytest.mark.asyncio
    async def test_find_one_shoe_by_id_fails_because_shoe_doesnt_exists(
            self,
            http_client: httpx.AsyncClient,
            ulid_generator: UlidProvider
    ) -> None:
        shoe_id = (await ulid_generator).generate()
        response = await http_client.get(f'/v1/shoes/{shoe_id.value}')
        assert response.status_code == 404
        assert response.json() == {"detail": "Shoe not exist."}

    @pytest.mark.asyncio
    async def test_find_one_shoe_by_id_fails_with_wrong_http_method(
            self,
            http_client: httpx.AsyncClient,
            ulid_generator: UlidProvider
    ) -> None:
        shoe_id = (await ulid_generator).generate()
        response = await http_client.delete(f'/v1/shoes/{shoe_id.value}')
        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}
