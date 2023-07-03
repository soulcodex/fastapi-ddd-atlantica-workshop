class RangeValue:

    def __init__(self, value: int, strict: bool = False):
        self.__value = value
        self.__strict = strict
        self.guard()

    @property
    def value(self):
        return self.__value

    def max_value(self) -> int:
        pass

    def min_value(self) -> int:
        pass

    def on_error(self) -> Exception:
        pass

    def error(self) -> None:
        on_error = self.on_error()
        if on_error is not None:
            raise on_error
        raise Exception({'message': 'Invalid value for range', 'value': self.value})

    def guard(self):
        min_value = self.min_value()
        max_value = self.max_value()

        if min_value is None and max_value is None:
            return

        if min_value is not None and max_value is None:
            if self.__strict and self.value < min_value:
                self.error()
            elif not self.value <= min_value:
                self.error()

        if min_value is None and max_value is not None:
            if self.__strict and self.value > max_value:
                self.error()
            elif not self.value >= max_value:
                self.error()

        if min_value is not None and max_value is not None:
            if self.__strict and self.value < min_value or self.value > max_value:
                self.error()
            elif not self.value <= min_value or not self.value >= max_value:
                self.error()
