import enum
from shoes.domain.errors import InvalidShoeSize
from shared.domain.types.boolean_value import BoolValue
from shared.domain.types.string_value import StringValue
from shared.domain.types.integer_value import RangeValue, IntegerValue, PriceValue


class ShoeName(StringValue):
    pass


class ShoeColor(enum.Enum):
    RED = 'red'
    GREEN = 'green'
    WHITE = 'white'
    BLACK = 'black'
    YELLOW = 'yellow'


class ShoePrice(PriceValue):
    pass


class ShoeActive(BoolValue):
    pass


class ShoeId(StringValue):
    pass


class ShoeSize(RangeValue):

    def max_value(self) -> int:
        return 45

    def min_value(self) -> int:
        return 34

    def on_error(self) -> Exception:
        return InvalidShoeSize.from_shoe_size(self.value)
