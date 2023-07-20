from typing import Union
from starlette import status
from dataclasses import asdict
from typing_extensions import Annotated
from apps.shoes.dependency_injection import shoes
from fastapi import APIRouter, HTTPException, Request, Depends
from apps.shoes.ui.shoe import Shoe, ShoeCollection, CreateShoe

from shoes.domain.types import ShoesQueryBus
from shoes.domain.errors import ShoeNotExist, InvalidShoeSize
from shoes.application import find_shoe_by_id, shoe_response

shoes_router = APIRouter(tags=['Shoes'])


@shoes_router.get('/{shoe_id}', response_model=Shoe, status_code=status.HTTP_200_OK)
async def get_shoe_by_id(shoe_id: str, qb: Annotated[ShoesQueryBus, Depends(shoes.shoes_query_bus)]):
    try:
        res: shoe_response.ShoeResponse = await qb.ask(find_shoe_by_id.FindShoeByIdQuery(shoe_id))
        return Shoe(**asdict(res))
    except ShoeNotExist or InvalidShoeSize as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@shoes_router.post('', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def create_one_shoe(_: CreateShoe):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Not implemented')
