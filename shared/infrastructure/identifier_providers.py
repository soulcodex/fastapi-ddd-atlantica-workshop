import uuid
import ulid

from typing import Optional

from shared.domain.types.identifier_providers import UuidProvider, UlidProvider, Uuid, Ulid


class RandomUuidProvider(UuidProvider):

    def generate(self) -> Uuid:
        identifier = uuid.uuid4()
        return Uuid(str(identifier))


class RandomUlidProvider(UlidProvider):

    def generate(self) -> Ulid:
        identifier = ulid.ULID()
        return Ulid(str(identifier))


class FixedUuidProvider(UuidProvider):

    def __init__(self):
        self._value: Optional[Uuid] = None

    def generate(self) -> Uuid:
        if self._value is not None:
            return self._value

        self._value = Uuid(str(uuid.uuid4()))
        return self._value


class FixedUlidProvider(UlidProvider):

    def __init__(self):
        self._value: Optional[Ulid] = None

    def generate(self) -> Ulid:
        if self._value is not None:
            return self._value

        self._value = Ulid(str(ulid.ULID()))
        return self._value
