from typing import Union
from starlette import status
from dataclasses import asdict
from pyxdi.ext.fastapi import Inject
from fastapi import APIRouter, HTTPException
from apps.shoes.ui.shoe import Shoe, ShoeCollection
from apps.shoes.dependency_injection.shoes_di import ShoesQueryBus

from shoes.domain.errors import ShoeNotExist, InvalidShoeSize
from shoes.application import find_shoe_by_id, shoe_response

shoes_router = APIRouter(tags=['Shoes'])


@shoes_router.get('/{shoe_id}', response_model=Shoe)
async def get_shoes_collection(shoe_id: str, qb: ShoesQueryBus = Inject()):
    try:
        res: shoe_response.ShoeResponse = await qb.ask(find_shoe_by_id.FindShoeByIdQuery(shoe_id))
        return Shoe(**asdict(res))
    except ShoeNotExist or InvalidShoeSize as e:
        raise HTTPException(status_code=404, detail=e.message)