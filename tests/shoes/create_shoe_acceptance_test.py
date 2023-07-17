import pytest
import pytest_asyncio
from pyxdi import PyxDI
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient
from typing import Dict, Text, Any, Callable, Coroutine

from shoes.domain.shoe import Shoe
from shared.domain.types.identifier_provider import UlidProvider

from shoes.infrastructure.pytest.factory import ShoeObjectMother
from shoes.infrastructure.pytest.fixtures import application, shoes_factory

ShoeJsonFactory = Callable[[Shoe], Dict[Text, Any]]


class TestCreateShoeAcceptance:

    @pytest_asyncio.fixture
    async def shoe_json_factory(self) -> ShoeJsonFactory:
        def _json(shoe: Shoe):
            return {
                "id": shoe.id.value,
                "color": shoe.color.value,
                "name": shoe.name.value,
                "available": shoe.available.value,
                "size": shoe.size.value,
                "price": shoe.price.raw_value,
            }

        return _json

    @pytest.mark.asyncio
    async def test_create_one_shoe_fails_because_route_doesnt_exists(
            self,
            application: FastAPI,
            shoes_factory: ShoeObjectMother,
            shoe_json_factory: ShoeJsonFactory
    ) -> None:
        async with AsyncClient(app=application, base_url='http://testserver') as client:
            random_shoe = shoes_factory.random_shoe()
            shoe_json = shoe_json_factory(random_shoe)

            response = await client.put(url='/v1/shoes', json=shoe_json)
            assert response.status_code == 405
            assert response.json() == {"detail": "Method Not Allowed"}

    @pytest.mark.asyncio
    async def test_create_one_random_shoe_successfully(
            self,
            application: FastAPI,
            shoes_factory: ShoeObjectMother,
            shoe_json_factory: ShoeJsonFactory
    ) -> None:
        async with AsyncClient(app=application, base_url='http://testserver') as client:
            random_shoe = shoes_factory.random_shoe()
            shoe_json = shoe_json_factory(random_shoe)
            response = await client.post(url='/v1/shoes', json=shoe_json)
            assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_create_one_shoe_fails_because_shoe_size_is_out_of_range(
            self,
            application: FastAPI,
            shoes_factory: ShoeObjectMother,
            shoe_json_factory: ShoeJsonFactory
    ) -> None:
        async with AsyncClient(app=application, base_url='http://testserver') as client:
            random_shoe = shoes_factory.random_shoe()
            shoe_json = shoe_json_factory(random_shoe)
            shoe_json.update({'size': 46})

            response = await client.post(url='/v1/shoes', json=shoe_json)
            assert response.status_code == 422
            assert response.json() == {
                'detail': [
                    {
                        'ctx': {'lt': 45},
                        'input': 46,
                        'loc': ['body', 'size'],
                        'msg': 'Input should be less than 45',
                        'type': 'less_than',
                        'url': 'https://errors.pydantic.dev/2.0.3/v/less_than'
                    }
                ]
            }

    @pytest.mark.asyncio
    async def test_create_one_shoe_fails_because_color_is_not_allowed(
            self,
            application: FastAPI,
            shoes_factory: ShoeObjectMother,
            shoe_json_factory: ShoeJsonFactory
    ) -> None:
        async with AsyncClient(app=application, base_url='http://testserver') as client:
            random_shoe = shoes_factory.random_shoe()
            shoe_json = shoe_json_factory(random_shoe)
            shoe_json.update({'color': 'pink'})

            response = await client.post(url='/v1/shoes', json=shoe_json)
            assert response.status_code == 422
            assert response.json() == {
                'detail': [
                    {
                        'ctx': {'expected': "'red','green','white','black' or 'yellow'"},
                        'input': 'pink',
                        'loc': ['body', 'color'],
                        'msg': "Input should be 'red','green','white','black' or 'yellow'",
                        'type': 'enum'
                    }
                ]
            }
