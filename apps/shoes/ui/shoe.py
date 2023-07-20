from pydantic import BaseModel, Field
from typing import Text, List, Optional, Any, Literal
from shoes.domain.value_object import ShoeColor, ShoeSize, ShoePrice

ULID_REGEX = r"[0-7][0-9A-HJKMNP-TV-Z]{25}"
ULID_EXAMPLES = ['01H5CNXSAWXWYCPRJ8515QFRBD']


class Shoe(BaseModel):
    id: Text = Field(examples=ULID_EXAMPLES, description='Shoe identifier as ULID', pattern=ULID_REGEX)
    name: Text = Field(max_length=50)
    color: Text
    size: int = Field(lt=ShoeSize.max_value(), gt=ShoeSize.min_value())
    price: Text
    available: bool


class CreateShoe(Shoe):
    color: ShoeColor
    price: int = Field(gt=ShoePrice.min_value(), description='Shoe price represented in cents')
    available: Optional[bool] = Field(default=True, examples=[True, False])


class ShoeCollection(BaseModel):
    items: List[Shoe]
