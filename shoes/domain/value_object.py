import enum
from typing import cast

from shared.domain.types.boolean_value import BoolValue
from shared.domain.types.integer_value import RangeValue, PriceValue
from shared.domain.types.string_value import StringValue
from shoes.domain.errors import InvalidShoeSize


class ShoeName(StringValue):
    pass


class ShoeColor(enum.Enum):
    RED = 'red'
    GREEN = 'green'
    WHITE = 'white'
    BLACK = 'black'
    YELLOW = 'yellow'


class ShoePrice(PriceValue):

    @staticmethod
    def min_value() -> int:
        return 499


class ShoeActive(BoolValue):
    pass


class ShoeId(StringValue):
    pass


class ShoeSize(RangeValue):

    @staticmethod
    def max_value() -> int:
        return 45

    @staticmethod
    def min_value() -> int:
        return 34

    def on_error(self) -> Exception:
        return cast(Exception, InvalidShoeSize.from_shoe_size(self.value))
