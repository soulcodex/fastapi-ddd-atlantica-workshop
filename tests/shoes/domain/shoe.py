from typing import Text
from shoes.domain.shoe import Shoe
from shoes.domain.value_object import ShoeId
from shared.domain.types.time_provider import TimeProvider
from shared.domain.types.identifier_provider import UlidProvider
from shared.infrastructure.time_providers import FixedTimeProvider
from shared.infrastructure.identifier_providers import FixedUlidProvider


class ShoeObjectMother:

    def __init__(self):
        self.identifier_provider: UlidProvider = FixedUlidProvider()
        self.time_provider: TimeProvider = FixedTimeProvider()

    def random_shoe(self) -> Shoe:
        shoe_id = ShoeId(self.identifier_provider.generate().value)
        now = self.time_provider.now()
        return Shoe.from_primitives(
            id=shoe_id.value,
            name='Nike',
            color='red',
            size=43,
            price=5600,
            available=True,
            created_at=now,
            updated_at=now
        )

    def with_size(self, size: int) -> Shoe:
        shoe = self.random_shoe()
        return Shoe.from_primitives(
            id=shoe.id.value,
            name=shoe.name.value,
            color=shoe.color.value,
            size=size,
            price=shoe.price.raw_value,
            available=shoe.available.value,
            created_at=shoe.created_at.value,
            updated_at=shoe.updated_at.value
        )

    def with_color(self, color: Text) -> Shoe:
        shoe = self.random_shoe()
        return Shoe.from_primitives(
            id=shoe.id.value,
            name=shoe.name.value,
            color=color,
            size=shoe.size.value,
            price=shoe.price.raw_value,
            available=shoe.available.value,
            created_at=shoe.created_at.value,
            updated_at=shoe.updated_at.value
        )

    def not_available(self) -> Shoe:
        shoe = self.random_shoe()
        return Shoe.from_primitives(
            id=shoe.id.value,
            name=shoe.name.value,
            color=shoe.color.value,
            size=shoe.size.value,
            price=shoe.price.raw_value,
            available=False,
            created_at=shoe.created_at.value,
            updated_at=shoe.updated_at.value
        )
