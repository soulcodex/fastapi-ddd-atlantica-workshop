class BoolValue:

    def __init__(self, value: bool):
        self.__value = value

    @property
    def value(self) -> bool:
        return self.__value

    def __eq__(self, other: "BoolValue"):
        return self.value == other.value
