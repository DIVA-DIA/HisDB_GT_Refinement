from __future__ import annotations
import operator
from dataclasses import dataclass, replace
from typing import Any, Tuple
import numpy as np

@dataclass(frozen=True)
class ImageDimension():

    width: int = 0
    height: int = 0

    def difference(self, other: Any) -> Tuple[float, float]:
        # division by two because we cut the same amount from top as from bottom
        return self.width - other.width, int((self.height - other.height) / 2)

    def to_tuple(self):
        return self.width, self.height

    # TODO: Delete if not used
    def img_dim_from_ndarray(self, array: np.ndarray) -> ImageDimension:
        """ Handles the conversion from the shape of an an ndarray :class: `np.ndarray` to ImageDimension.
        :param numpy_array:
        :return:
        """
        shape = array.shape
        return ImageDimension(width=shape[1],height=shape[0])

    def scale_factor(self, other: ImageDimension):
        return self.width / other.width, self.height / other.height

    def _scale(self, scale_factor: Tuple[float,float]):
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

    def __str__(self):
        return "ImageDimension /n width = {} /n height = {}".format(self.width, self.height)
