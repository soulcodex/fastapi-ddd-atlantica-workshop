from typing import Optional
from datetime import datetime, timezone
from shared.domain.types.time_provider import TimeProvider


class SystemTimeProvider(TimeProvider):

    def now(self) -> datetime:
        return datetime.now().replace(tzinfo=timezone.utc)


class FixedTimeProvider(TimeProvider):

    def __init__(self):
        self._value: Optional[datetime] = None

    def now(self) -> datetime:
        if self._value is not None:
            return self._value

        self._value = datetime.now().replace(tzinfo=timezone.utc)
        return self._value
