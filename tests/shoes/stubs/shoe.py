from shoes.domain.shoe import Shoe
from shoes.domain.value_object import ShoeId
from shared.domain.types.time_provider import TimeProvider
from shared.domain.types.identifier_provider import UlidProvider
from shared.infrastructure.time_providers import FixedTimeProvider
from shared.infrastructure.identifier_providers import FixedUlidProvider


class ShoeMother:

    def __init__(self):
        self.identifier_provider: UlidProvider = FixedUlidProvider()
        self.time_provider: TimeProvider = FixedTimeProvider()

    def random_shoe(self) -> Shoe:
        shoe_id = ShoeId(self.identifier_provider.generate().value)
        now = self.time_provider.now()
        return Shoe.from_primitives(
            shoe_id=shoe_id.value,
            name='Nike',
            color='red',
            size=43,
            price=5600,
            available=True,
            created_at=now,
            updated_at=now
        )
