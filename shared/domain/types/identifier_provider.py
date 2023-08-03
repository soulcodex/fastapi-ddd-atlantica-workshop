from abc import ABC, abstractmethod


class Uuid(str):

    @property
    def value(self) -> str:
        return str(self)

    def __eq__(self, other: "Uuid") -> bool:
        return self.value == other.value


class Ulid(str):

    @property
    def value(self) -> str:
        return str(self)

    def __eq__(self, other: "Ulid") -> bool:
        return self.value == other.value


class UuidProvider(ABC):

    @abstractmethod
    def generate(self) -> Uuid:
        pass


class UlidProvider(ABC):

    @abstractmethod
    def generate(self) -> Ulid:
        pass
