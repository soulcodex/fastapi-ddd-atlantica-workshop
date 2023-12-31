import httpx
import pytest
import pytest_asyncio
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
            http_client: httpx.AsyncClient,
            shoes_factory: ShoeObjectMother,
            shoe_json_factory: ShoeJsonFactory
    ) -> None:
        random_shoe = shoes_factory.random_shoe()
        shoe_json = shoe_json_factory(random_shoe)

        response = await http_client.put(url='/v1/shoes', json=shoe_json)
        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}

    @pytest.mark.asyncio
    async def test_create_one_random_shoe_successfully(
            self,
            http_client: httpx.AsyncClient,
            shoes_factory: ShoeObjectMother,
            shoe_json_factory: ShoeJsonFactory
    ) -> None:
        random_shoe = shoes_factory.random_shoe()
        shoe_json = shoe_json_factory(random_shoe)
        response = await http_client.post(url='/v1/shoes', json=shoe_json)
        assert response.status_code == 204
        shoe_response = await http_client.get(url=f'/v1/shoes/{random_shoe.id.value}')
        assert shoe_response.status_code == 200
        shoe_response_json = shoe_response.json()
        assert shoe_response_json.get('id') == random_shoe.id.value
        assert shoe_response_json.get('name') == random_shoe.name.value

    @pytest.mark.asyncio
    async def test_create_one_shoe_fails_because_shoe_size_is_out_of_range(
            self,
            http_client: httpx.AsyncClient,
            shoes_factory: ShoeObjectMother,
            shoe_json_factory: ShoeJsonFactory
    ) -> None:
        random_shoe = shoes_factory.random_shoe()
        shoe_json = shoe_json_factory(random_shoe)
        shoe_json.update({'size': 46})

        response = await http_client.post(url='/v1/shoes', json=shoe_json)
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
            http_client: httpx.AsyncClient,
            shoes_factory: ShoeObjectMother,
            shoe_json_factory: ShoeJsonFactory
    ) -> None:
        random_shoe = shoes_factory.random_shoe()
        shoe_json = shoe_json_factory(random_shoe)
        shoe_json.update({'color': 'pink'})

        response = await http_client.post(url='/v1/shoes', json=shoe_json)
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
