import os
from fastapi import APIRouter
from fastapi_injector import Injected
from shared.domain.bus.query_bus import QueryBus
from apps.shoes.ui.beer import Beer, BeerCollection
from apps.shoes.routes.query_params import pagination as pagination_injector

shoes_router = APIRouter(tags=['Shoes'])


@shoes_router.get('')
async def get_shoes_collection(query_bus: QueryBus = Injected(QueryBus)) -> BeerCollection:
    try:
        pass
    except Exception as e:
        print(e)
    return BeerCollection(items=[], count=[].__len__())


@shoes_router.post('')
async def create_shoe_item(page: int = 1, per_page: int = 10) -> BeerCollection:
    return BeerCollection(items=[], count=[].__len__())
