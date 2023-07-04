from typing import Text
from dataclasses import dataclass
from shoes.domain.shoe import Shoe


@dataclass
class ShoeResponse:
    id: Text
    name: Text
    color: Text
    size: Text
    price: Text
    available: bool

    @classmethod
    def from_shoe(cls, shoe: Shoe) -> 'ShoeResponse':
        return cls(
            id=shoe.id.value,
            name=shoe.name.value,
            color=shoe.color.value,
            size=shoe.size.value_string,
            price=shoe.price.value_with_currency('€'),
            available=shoe.available.value
        )
