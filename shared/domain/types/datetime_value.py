from datetime import datetime, timezone
from shared.domain.utils import datetime_to_milliseconds


class Timestamp:

    def __init__(self, value: datetime):
        self.__value = value

    @property
    def value(self) -> datetime:
        return self.__value

    @property
    def timestamp(self) -> float:
        return self.__value.timestamp()

    @property
    def millis(self) -> int:
        return datetime_to_milliseconds(self.__value)

    def __eq__(self, other: "Timestamp"):
        return self.value == other.value


class CreatedAt(Timestamp):
    pass


class UpdatedAt(Timestamp):
    pass
