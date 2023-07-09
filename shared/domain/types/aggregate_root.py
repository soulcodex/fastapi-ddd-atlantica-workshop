from typing import List
from shared.domain.types.domain_event import DomainEvent


class AggregateRoot:
    events: List[DomainEvent] = []

    def record(self, event: DomainEvent) -> None:
        self.events.append(event)

    def pull_events(self) -> List[DomainEvent]:
        return self.events
