from typing import Optional, Text


class RangeValue:

    def __init__(self, value: int):
        self._value = value
        self.guard()

    @property
    def value(self):
        return self._value

    @property
    def value_string(self):
        return str(self.value)

    @staticmethod
    def max_value() -> int:
        pass

    @staticmethod
    def min_value() -> int:
        pass

    def on_error(self) -> Exception:
        pass

    def error(self) -> None:
        on_error = self.on_error()
        if on_error is not None:
            raise on_error
        raise Exception({'message': 'Invalid value for range', 'value': self.value})

    def __eq__(self, other: 'RangeValue'):
        return self.value == other.value

    def guard(self):
        min_value = self.min_value()
        max_value = self.max_value()

        if min_value is None and max_value is None:
            return

        if min_value is not None and max_value is None and not self.value >= min_value:
            self.on_error()

        if min_value is None and max_value is not None and self.value > max_value:
            self.on_error()

        if min_value is not None and max_value is not None:
            if not self.value >= min_value or self.value > max_value:
                self.on_error()


class IntegerValue:

    def __init__(self, value: int):
        self._value = value
        self.guard()

    @property
    def value(self) -> int:
        return self._value

    def guard(self) -> None:
        pass

    def __eq__(self, other: 'IntegerValue'):
        return self.value == other.value


class OptionalIntegerValue:

    def __init__(self, value: Optional[int] = None):
        self._value = value
        self.guard()

    @property
    def value(self) -> Optional[int]:
        return self._value

    def guard(self) -> None:
        pass

    def __eq__(self, other: 'OptionalIntegerValue'):
        return self.value == other.value


class PriceValue(IntegerValue):

    @property
    def value(self) -> float:
        return self._value / 100

    @property
    def raw_value(self) -> int:
        return self._value

    def value_with_currency(self, currency_symbol: Text):
        return f'{self.value:.2f} {currency_symbol}'
