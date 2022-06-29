from __future__ import annotations
import operator
from typing import List, Tuple
from scipy.spatial import distance as dist
import numpy as np
from PIL import ImageDraw

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GTInterfaces import Scalable, Drawable, Croppable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension


class Polygon(Scalable, Drawable, Croppable):
    """ This class is the parent class of all vector objects used in to represent the vector ground truth.
    :param xy: is a polygon of 2 or more coordinates.
    :type xy: represents the coordinates [(x1,x1),(x2,y2),...] of the polygon. It's important the polygon is sorted.
    No checks are made for that. It doesn't matter if the polygon is closed or open (the last coordinate doesn't need to
    be the first coordinate).
    """

    def __init__(self, xy: List[Tuple]):
        if len(xy) < 2:
            raise AttributeError("xy is not a polygon: " + str(xy))
        self.xy: List[Tuple] = xy

    def draw(self, drawer: ImageDraw, outline=(255, 255, 255), fill=None):
        drawer.polygon(xy=self.xy, outline=outline, fill=fill)

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        scale_factor: Tuple[float, float] = current_dim.scale_factor(target_dim)
        self.xy = [tuple(map(operator.truediv, t, scale_factor)) for t in self.xy]
        self.xy = [tuple(map(round, t)) for t in self.xy]

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        difference = current_dim.difference(target_dim)
        if not cut_left:
            difference = (0, difference[1])
        self.xy = self._find_and_scale_points(difference)

    def _find_and_scale_points(self, difference: Tuple[float, float]):
        return [tuple(map(operator.sub, t, difference)) for t in self.xy]

    def get_bbox(self) -> Rectangle:
        bbox: Rectangle = Rectangle([(self.get_min_x(), self.get_min_y()), (self.get_max_x(), self.get_max_y())])
        return bbox

    def get_min_x(self):
        min_x = float("inf")
        for coord in self.xy:
            if coord[0] < min_x:
                min_x = int(coord[0])
        return min_x

    def get_min_y(self):
        min_y = float("inf")
        for coord in self.xy:
            if coord[1] < min_y:
                min_y = int(coord[1])
        return min_y

    def get_max_x(self):
        max_x = 0
        for coord in self.xy:
            if coord[0] > max_x:
                max_x = int(coord[0])
        return max_x

    def get_max_y(self):
        max_y = 0
        for coord in self.xy:
            if coord[1] > max_y:
                max_y = int(coord[1])
        return max_y


class Quadrilateral(Polygon):
    """
    :param xy: 4 coords that represent a quadrilateral. which are sorted upon initialisation to ensure a useful representation with the draw method.
    representation with the draw method.
    """

    def __init__(self, xy: List[Tuple]):
        sorted_xy = self._order_points(xy)
        super().__init__(sorted_xy)
        assert len(xy) == 4

    def _order_points(self, xy):
        # sort the points based on their x-coordinates
        as_np_array = np.asarray(xy)
        xSorted = as_np_array[np.argsort(as_np_array[:, 0]), :]
        # grab the left-most and right-most points from the sorted
        # x-roodinate points
        leftMost = xSorted[:2, :]
        rightMost = xSorted[2:, :]
        # now, sort the left-most coordinates according to their
        # y-coordinates so we can grab the top-left and bottom-left
        # points, respectively
        leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
        (tl, bl) = leftMost
        # now that we have the top-left coordinate, use it as an
        # anchor to calculate the Euclidean distance between the
        # top-left and right-most points; by the Pythagorean
        # theorem, the point with the largest distance will be
        # our bottom-right point
        D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
        (br, tr) = rightMost[np.argsort(D)[::-1], :]
        # return the coordinates in top-left, top-right,
        # bottom-right, and bottom-left order
        return [tuple(tl), tuple(tr), tuple(br), tuple(bl)]

    def draw(self, drawer: ImageDraw, outline=(255, 125, 0), fill=None):
        drawer.polygon(self.xy, outline=outline, fill=fill)


class Rectangle(Polygon):
    def __init__(self, xy):
        super().__init__(xy=xy)
        assert len(xy) == 2

    def draw(self, drawer: ImageDraw, outline=(225, 225, 10), fill=None):
        drawer.rectangle(self.xy, outline=outline, fill=fill)


class Line(Polygon):
    def __init__(self, xy):
        super().__init__(xy=xy)
        assert len(xy) == 2

    def draw(self, drawer: ImageDraw, outline=None, fill=(0, 125, 255)):
        drawer.line(self.xy, fill=fill)
