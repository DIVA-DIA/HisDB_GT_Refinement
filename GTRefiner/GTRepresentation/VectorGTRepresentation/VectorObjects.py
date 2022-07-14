from __future__ import annotations
import operator
import warnings
from typing import List, Tuple
from scipy.spatial import distance as dist
import numpy as np
from PIL import ImageDraw
from copy import deepcopy

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Scalable, Drawable, Croppable, \
    Dictionable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension

# TODO: outline wird immer None sein. outline wegnehmen.
# TODO: Import shapely -> wäre toll.

class Polygon(Scalable, Drawable, Croppable, Dictionable):
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
        for elem in xy:
            if isinstance(elem[0], np.int64) or isinstance(elem[1], np.int64):
                raise ValueError("Should be of python integer at instantiation")

    def draw(self, drawer: ImageDraw, color: Tuple = None):
        drawer.polygon(xy=self.xy, outline=None, fill=color)

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
        return [(x - difference[0], y - difference[1]) for x, y in self.xy]
        #return [tuple(map(operator.sub, t, difference)) for t in self.xy]


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

    def __getitem__(self, index):
        return self.xy[index]

    def __eq__(self, other):
        if not isinstance(other, Polygon):
            return False
        if not len(self.xy) == len(other.xy):
            return False
        for i, coord in enumerate(other.xy):
            if not coord[0] == self.xy[i][0]:
                return False
            if not coord[1] == self.xy[i][1]:
                return False
        return True




class Quadrilateral(Polygon):
    """
    :param xy: 4 coords that represent a quadrilateral. which are sorted upon initialisation to ensure a useful representation with the draw method.
    representation with the draw method.
    """

    def __init__(self, xy: List[Tuple]):
        sorted_xy = self._order_points(xy)
        super().__init__(sorted_xy)
        assert len(xy) == 4

    @classmethod
    def _order_points(cls, xy):
        # TODO: Make sure that this function works fine.
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
        sorted_points = [tuple(tl), tuple(tr), tuple(br), tuple(bl)]
        sorted_points_to_python_int = [(coord[0].item(), coord[1].item()) for coord in sorted_points]
        return sorted_points_to_python_int

    def is_sorted(self):
        sorted = self._order_points(deepcopy(self.xy))
        return sorted == self.xy

    def draw(self, drawer: ImageDraw, color=None):
        drawer.polygon(self.xy, outline=None, fill=color)


class Rectangle(Polygon):
    def __init__(self, xy):
        super().__init__(xy=xy)
        assert len(xy) == 2

    def draw(self, drawer: ImageDraw, color: Tuple = None):
        drawer.rectangle(self.xy, outline=None, fill=color)


class Line(Polygon):
    def __init__(self, xy):
        super().__init__(xy=xy)
        assert len(xy) == 2

    def draw(self, drawer: ImageDraw, outline=None, color: Tuple = None):
        """ Draws a line."""
        if outline is None:
            warnings.warn("The Line vector object doesn't provide an outline due to it's nature. Use 'fill' to specify "
                          "the color of the line. Fill default = (0, 125, 255)")
        drawer.line(self.xy, fill=color)

    def get_min_x_coord(self):
        return self.xy[0]

    def get_max_x_coord(self):
        return self.xy[1]


