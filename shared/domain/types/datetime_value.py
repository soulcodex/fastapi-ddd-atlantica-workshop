from datetime import datetime, timezone


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
    def millis(self) -> float:
        return self.__value.replace(tzinfo=timezone.utc).timestamp() * 1000

    def __eq__(self, other: 'Timestamp'):
        return self.value == other.value


class CreatedAt(Timestamp):
    pass


class UpdatedAt(Timestamp):
    pass
