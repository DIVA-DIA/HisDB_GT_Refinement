import operator
from dataclasses import dataclass, replace
from typing import Any, Tuple


# TODO: It's a bit confusing that height, width is the order to instantiate, but width, height is what we get back.
@dataclass(frozen=True)
class ImageDimension:
    height: int = 0
    width: int = 0

    def difference(self, other: Any) -> Tuple[float, float]:
        # division by two because we cut the same amount from top as from bottom
        return self.width - other.width, int((self.height - other.height) / 2)

    def to_tuple(self):
        return self.width, self.height

    def scale_factor(self, other: Any):
        return self.width / other.width, self.height / other.height

    def scale(self, scale_factor: Tuple[float,float]):
        height = round(operator.truediv(self.height, scale_factor[1]))
        width = round(operator.truediv(self.width, scale_factor[0]))
        return ImageDimension(width=width, height=height)

    def __eq__(self, other):
        if type(self) is type(other):
            if self.height == other.height:
                if self.width == other.width:
                    return True
        else:
            return False



if __name__ == '__main__':
    dimension_1 = ImageDimension(300,500)
    dimension_2 = ImageDimension(200,333)

    print("imension_1.difference(dimension_2):")
    print(dimension_1.difference(dimension_2))
    print("imension_1.scale_factor(dimension_2):")
    print(dimension_1.scale_factor(dimension_2))

    print("dimension_2.difference(dimension_1):")
    print(dimension_2.difference(dimension_1))
    print("dimension_2.scale_factor(dimension_1):")
    print(dimension_2.scale_factor(dimension_1))


    as_tuple = dimension_1.to_tuple()

    print("as tuple:" + str(as_tuple))

    print(dimension_1.width)
    print(dimension_1.height)
