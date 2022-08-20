from __future__ import annotations
import operator
import warnings
from dataclasses import dataclass, replace
from typing import Any, Tuple
import numpy as np


@dataclass(frozen=True)
class ImageDimension():
    width: int = 0
    height: int = 0

    def difference(self, other: ImageDimension) -> Tuple[float, float]:
        """ Method used solely for cropping. Calculates the difference for which a vector object has to be moved given another target dimension.
        :param other: other dimension
        :type other: ImageDimension
        :return: the difference in x,y as float tuple.
        :rtype: tuple
        """
        # division by two because we cut the same amount from top as from bottom
        return self.width - other.width, int((self.height - other.height) / 2)

    def to_tuple(self):
        """ Get the dimension as a tuple
        :return: Width and height
        :rtype: tuple
        """
        return self.width, self.height

    def scale_factor(self, other: ImageDimension):
        """Helper method for resizing. Gives the scale factor for which a given ground truth object should be resized.
        :param other: target dimension.
        :type other: ImageDimension
        :return: list of width scale factor and height scale factor
        :rtype:
        """
        width_scale_factor = self.width / other.width
        height_scale_factor = self.height / other.height
        if width_scale_factor != height_scale_factor:
            warnings.warn("The target dimension and current dimension do not have maching proportions.")
        check_w_s = int(width_scale_factor) - width_scale_factor
        check_h_s = int(height_scale_factor) - width_scale_factor
        if check_w_s != 0 or check_h_s != 0:
            warnings.warn("The target dimension or current dimension are not integer divider. "
                          "Might lead to weird scaling artifacts.")
        return width_scale_factor, height_scale_factor

    def _scale(self, scale_factor: Tuple[float, float]):
        height = round(operator.truediv(self.height, scale_factor[1]))
        width = round(operator.truediv(self.width, scale_factor[0]))
        return ImageDimension(width=width, height=height)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        if self.height != other.height:
            return False
        if self.width != other.width:
            return False
        return True

    def __str__(self):
        return "ImageDimension /n width = {} /n height = {}".format(self.width, self.height)
