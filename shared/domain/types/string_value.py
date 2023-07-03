from typing import Text


class StringValue:

    def __init__(self, value: Text):
        self.__value = value
        self.guard()

    def guard(self) -> None:
        pass

    @property
    def value(self):
        return self.__value
