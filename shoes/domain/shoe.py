from typing import Text
from abc import ABC, abstractmethod
from shoes.domain.value_object import ShoeId, ShoeName, ShoeSize


class Shoe:

    def __init__(self, shoe_id: ShoeId, name: ShoeName, size: ShoeSize):
        self.id = shoe_id
        self.name = name
        self.size = size

    @classmethod
    def from_primitives(cls, shoe_id: str, name: str, size: int) -> 'Shoe':
        return cls(shoe_id=ShoeId(shoe_id), name=ShoeName(name), size=ShoeSize(size))


class ShoeRepository(ABC):

    @abstractmethod
    def find(self, shoe_id: ShoeId) -> Shoe:
        pass
