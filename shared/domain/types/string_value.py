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

    def __eq__(self, other: "StringValue"):
        return other.value == self.__value
