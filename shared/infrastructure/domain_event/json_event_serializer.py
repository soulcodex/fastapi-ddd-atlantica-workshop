import json
from typing import Text
from shared.domain.utils import datetime_to_milliseconds
from shared.domain.types.domain_event import DomainEventSerializer, DomainEvent


class JsonDomainEventSerializer(DomainEventSerializer):

    def __init__(self, service: Text):
        self.service = service

    async def serialize(self, event: DomainEvent) -> Text:
        attributes = event.payload
        attributes['id'] = event.aggregate_id.value

        json_event = {
            'data': {
                'id': event.id.value,
                'type': event.event_name(),
                'attributes': attributes
            },
            'meta': {
                'created_at': datetime_to_milliseconds(event.occurred_on),
                'service': self.service
            }
        }
        return json.dumps(obj=json_event, indent=None)
