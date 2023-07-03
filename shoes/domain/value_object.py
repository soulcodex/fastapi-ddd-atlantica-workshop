from shoes.domain.errors import InvalidShoeSize
from shared.domain.types.string_value import StringValue
from shared.domain.types.integer_range_value import RangeValue


class ShoeName(StringValue):
    pass


class ShoeId(str):
    pass


class ShoeSize(RangeValue):

    def max_value(self) -> int:
        return 45

    def min_value(self) -> int:
        return 34

    def on_error(self) -> Exception:
        return InvalidShoeSize.from_shoe_size(self.value)
