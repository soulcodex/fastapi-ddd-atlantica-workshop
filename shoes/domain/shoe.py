from typing import Text
from datetime import datetime
from abc import ABC, abstractmethod
from shared.domain.types.aggregate_root import AggregateRoot
from shared.domain.types.datetime_value import CreatedAt, UpdatedAt
from shoes.domain.value_object import ShoeId, ShoeName, ShoeSize, ShoeColor, ShoePrice, ShoeActive


class Shoe(AggregateRoot):

    def __init__(
            self,
            shoe_id: ShoeId,
            name: ShoeName,
            color: ShoeColor,
            size: ShoeSize,
            price: ShoePrice,
            available: ShoeActive,
            created_at: CreatedAt,
            updated_at: UpdatedAt
    ):
        self.id = shoe_id
        self.name = name
        self.color = color
        self.size = size
        self.price = price
        self.available = available
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_primitives(
            cls,
            shoe_id: str,
            name: str,
            color: str,
            size: int,
            price: int,
            available: bool,
            created_at: datetime,
            updated_at: datetime
    ) -> 'Shoe':
        return cls(
            shoe_id=ShoeId(shoe_id),
            name=ShoeName(name),
            color=ShoeColor(color),
            size=ShoeSize(size),
            price=ShoePrice(price),
            available=ShoeActive(available),
            created_at=CreatedAt(created_at),
            updated_at=UpdatedAt(updated_at)
        )


class ShoesRepository(ABC):

    @abstractmethod
    async def find(self, shoe_id: ShoeId) -> 'Shoe':
        pass
