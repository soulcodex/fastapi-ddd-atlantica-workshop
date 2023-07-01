from abc import ABC, abstractmethod


class Dto(ABC):

    @staticmethod
    @abstractmethod
    def id() -> str:
        pass


class InvalidDto(Exception):

    def __init__(self, message: str):
        self.message = message
