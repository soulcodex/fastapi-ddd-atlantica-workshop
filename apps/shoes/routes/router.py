from dataclasses import asdict

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from typing_extensions import Annotated

from apps.shoes.dependency_injection import shoes
from apps.shoes.ui.shoe import Shoe, CreateShoe
from shoes.application import find_shoe_by_id, create_shoe, shoe_response
from shoes.domain.errors import ShoeNotExist, InvalidShoeSize
from shoes.domain.types import ShoesQueryBus, ShoesCommandBus

shoes_router = APIRouter(tags=['Shoes'])


@shoes_router.get('/{shoe_id}', response_model=Shoe, status_code=status.HTTP_200_OK)
async def get_shoe_by_id(shoe_id: str, query_bus: Annotated[ShoesQueryBus, Depends(shoes.shoes_query_bus)]):
    try:
        res: shoe_response.ShoeResponse = await query_bus.ask(find_shoe_by_id.FindShoeByIdQuery(shoe_id))
        return Shoe(**asdict(res))
    except ShoeNotExist as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except InvalidShoeSize as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@shoes_router.post('', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def create_one_shoe(
        shoe: CreateShoe,
        command_bus: Annotated[ShoesCommandBus, Depends(shoes.shoes_command_bus)]
) -> None:
    try:
        command = create_shoe.CreateShoeCommand(
            shoe_id=shoe.id, name=shoe.name, color=shoe.color.value,
            size=shoe.size, price=shoe.price, available=shoe.available
        )
        await command_bus.dispatch(command)
    except InvalidShoeSize as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())
