import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Text, Dict, Any, Optional, Union
from shared.domain.types.identifier_provider import Uuid, Ulid


class DomainEvent(ABC):
    def __init__(
            self,
            aggregate_id: Union[Uuid, Ulid],
            payload: Dict[Text, Any],
            _id: Optional[Uuid] = None,
            occurred_on: Optional[datetime] = None,
            metadata: Optional[Dict[Text, Any]] = None,
    ):
        self.id = Uuid(uuid.uuid4().__str__()) if _id is None else _id
        self.aggregate_id = aggregate_id
        self.payload = payload
        self.occurred_on = occurred_on if occurred_on is not None else datetime.now()
        self.metadata = metadata if metadata is not None else {}

    def add_metadata(self, metadata: Dict[Text, Any]):
        for key, content in metadata.items():
            self.metadata[key] = content

    @abstractmethod
    def event_name(self) -> Text:
        pass

    def __repr__(self) -> Text:
        return f'<{self.__class__.__name__} {self.id.value}> ({self.payload}) ({self.metadata})'


class ConsumableDomainEvent:

    @abstractmethod
    def aggregate_id(self) -> Uuid:
        pass

    @classmethod
    @abstractmethod
    async def from_raw(cls, payload: Dict[Text, Any]) -> 'ConsumableDomainEvent':
        pass


class DomainEventSerializer(ABC):

    @abstractmethod
    async def serialize(self, event: DomainEvent) -> Text:
        pass


class DomainEventPublisher(ABC):

    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        pass
