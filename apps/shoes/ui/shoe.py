from pydantic import BaseModel, Field
from typing import Text, List, Optional, Any


class Shoe(BaseModel):
    id: Text
    name: Text
    color: Text
    size: Text
    price: Text
    available: bool


class ShoeCollection(BaseModel):
    items: List[Shoe]
