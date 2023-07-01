import os
from os import environ
from typing import Any, Text
from abc import ABC, abstractmethod


class EnvironmentHandler(ABC):

    @abstractmethod
    def get_value(self, key: Text) -> Any:
        pass

    @abstractmethod
    def set_value(self, key: Text, value: Text) -> None:
        pass


class NativeEnvironmentHandler(EnvironmentHandler):

    def get_value(self, key: Text) -> Any:
        if key in os.environ:
            return os.environ[key]

    def set_value(self, key: Text, value: Text) -> None:
        os.environ[key] = value
