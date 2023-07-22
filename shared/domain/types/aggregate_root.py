from typing import List
from shared.domain.types.domain_event import DomainEvent


class EventRecorder:
    events: List[DomainEvent] = []

    def record(self, event: DomainEvent) -> None:
        self.events.append(event)

    def pull_events(self) -> List[DomainEvent]:
        events = self.events
        self.events = []
        return events


class AggregateRoot(EventRecorder):
    pass
