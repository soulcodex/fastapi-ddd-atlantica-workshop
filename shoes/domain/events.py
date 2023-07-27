from typing import Text, Dict, Any
from shared.domain.types.identifier_provider import Uuid
from shared.domain.utils import datetime_to_milliseconds
from shared.domain.types.domain_event import DomainEvent


class ShoeCreated(DomainEvent):

    def event_name(self) -> Text:
        return 'atlantica.shoes_api.shoe_created'

    @classmethod
    def from_shoe(cls, shoe: "Shoe") -> "ShoeCreated":
        return cls(
            aggregate_id=shoe.id.value,
            payload={
                'name': shoe.name.value,
                'color': shoe.color.value,
                'size': shoe.size.value,
                'price': shoe.price.raw_value,
                'available': shoe.available.value,
                'created_at': datetime_to_milliseconds(shoe.created_at.value)
            }
        )


class ShoeUpdated(DomainEvent):

    def event_name(self) -> Text:
        return 'atlantica.shoes_api.shoe_updated'

    @classmethod
    def from_shoe(cls, shoe: "Shoe") -> "ShoeUpdated":
        return cls(
            aggregate_id=shoe.id.value,
            payload={
                'name': shoe.name.value,
                'color': shoe.color.value,
                'size': shoe.size.value,
                'price': shoe.price.raw_value,
                'available': shoe.available.value,
                'updated_at': datetime_to_milliseconds(shoe.updated_at.value)
            }
        )
