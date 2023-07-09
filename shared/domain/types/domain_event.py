from datetime import datetime
from abc import ABC, abstractmethod
from typing import Text, Dict, Any, Optional, Union
from shared.domain.types.identifier_provider import Uuid, Ulid


class DomainEvent(ABC):

    def __init__(
            self,
            _id: Uuid,
            aggregate_id: Union[Uuid, Ulid],
            payload: Dict[Text, Any],
            occurred_on: Optional[datetime] = None,
            metadata: Optional[Dict[Text, Any]] = None,
    ):
        self.id = _id
        self.aggregate_id = aggregate_id
        self.payload = payload
        self.occurred_on = occurred_on if occurred_on is not None else datetime.now()
        self.metadata = metadata if metadata is not None else {}

    def add_metadata(self, metadata: Dict[Text, Any]):
        for key, content in metadata.items():
            self.metadata[key] = content


class ConsumableDomainEvent(DomainEvent):

    @abstractmethod
    def aggregate_id(self) -> Uuid:
        pass

    @abstractmethod
    def from_raw(self, payload: Dict[Text, Any]) -> 'DomainEventConsumable':
        pass
