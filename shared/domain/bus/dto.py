from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Dto(ABC):

    @staticmethod
    @abstractmethod
    def id() -> str:
        pass


class InvalidDto(Exception):

    def __init__(self, message: str):
        self.message = message
