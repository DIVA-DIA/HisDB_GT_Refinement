from __future__ import annotations

import operator
import warnings
from typing import List, Tuple

import numpy as np
from PIL import ImageDraw
from scipy.spatial import distance as dist

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Scalable, Drawable, Croppable, \
    Dictionable

class Polygon(Scalable, Drawable, Croppable, Dictionable):
    """ This class is the parent class of all vector objects used to represent the vector ground truth.
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

    def draw(self, drawer: ImageDraw, color: Tuple = None, outline: Tuple = None):
        """ Draw the vector object on a given object.
        :param drawer: Pillow drawer, can be of any mode (example "1", "RGB", "RGBA"). The color parameter must be corresponding format.
        :type drawer: ImageDraw.ImageDraw
        :param color: Single element tuple for binary, triple tuple for RGB, quadruple tuple for RGBA (consult PILLOW Documenation for more information).
        :type color: tuple
        :param outline: Only use this parameter for illustration purposes. Using it for ground truth generation is dangerous.
        :type outline: tuple
        :return:
        :rtype:
        """
        drawer.polygon(xy=self.xy, outline=outline, fill=color)

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        """Resizes the vector object to a given target
        dimension. As this class doesn't possess a image dimension parameter, both the current dimension (of the page)
        and the target dimension (the size to be scaled to) must be given.
        :param current_dim: Current dimension
        :type current_dim: ImageDimension
        :param target_dim: Target dimension
        :type target_dim: ImageDimension
        """
        scale_factor: Tuple[float, float] = current_dim.scale_factor(target_dim)
        self.xy = [tuple(map(operator.truediv, t, scale_factor)) for t in self.xy]
        self.xy = [tuple(map(round, t)) for t in self.xy]

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        """ Crop this vector object to a target dimension. Due to the nature of the ground truth document
        :param cut_left: must be provided.
        :param current_dim: Current dimension
        :type current_dim: ImageDimension
        :param target_dim: Target dimension
        :type target_dim: ImageDimension
        :param cut_left: Whether or not the page is cut_left or not.
        :type cut_left: bool
        """
        difference = current_dim.difference(target_dim)
        if not cut_left:
            difference = (0, difference[1])
        self.xy = self._find_and_scale_points(difference)

    def _find_and_scale_points(self, difference: Tuple[float, float]):
        """  Helper method for crop().
        :param difference: Move the points with the given difference.
        :type difference: Tuple[int, int]
        :return: returns the moved (cropped) coordinates of xy.
        :rtype: tuple
        """
        return [(x - difference[0], y - difference[1]) for x, y in self.xy]
        # return [tuple(map(operator.sub, t, difference)) for t in self.xy]

    def get_bbox(self) -> Rectangle:
        """ Get bounding box of the vector object.
        :return: returns a rectangle defining the bounding box.
        :rtype: Rectangle
        """
        bbox: Rectangle = Rectangle([(self.get_min_x(), self.get_min_y()), (self.get_max_x(), self.get_max_y())])
        return bbox

    def get_min_x(self):
        """ Get min x coordinate of all the coordinates of this vector object.
        :return: min x
        :rtype: int
        """
        min_x = float("inf")
        for coord in self.xy:
            if coord[0] < min_x:
                min_x = int(coord[0])
        return min_x

    def get_min_y(self):
        """ Get min y coordinate of all the coordinates of this vector object.
        :return: min y
        :rtype: int
        """
        min_y = float("inf")
        for coord in self.xy:
            if coord[1] < min_y:
                min_y = int(coord[1])
        return min_y

    def get_max_x(self):
        """ Get max x coordinate of all the coordinates of this vector object.
        :return: max x
        :rtype: int
        """
        max_x = 0
        for coord in self.xy:
            if coord[0] > max_x:
                max_x = int(coord[0])
        return max_x

    def get_max_y(self):
        """ Get max y coordinate of all the coordinates of this vector object.
        :return: max y
        :rtype: int
        """
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
        # sorted_xy = self._order_points(xy)
        super().__init__(xy)
        assert len(xy) == 4
        if not self.is_sorted():
            warnings.warn(f"Xy is not sorted.{xy}")
            temp = self.xy[2]
            self.xy[2] = self.xy[3]
            self.xy[3] = temp

    @classmethod
    def _order_points(cls, xy):
        """ Order the points of a rectangle. This method was tested, but we can guarantee of it's proper function 100%.
        :param xy: 4 coordinates to be sorted.
        :type xy: tuple
        :return: sorted coords (left upper, right upper, right lower, left lower)
        :rtype: tuple
        """
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
        if not self.xy[0][1] < self.xy[3][1]:
            return False
        if not self.xy[1][1] < self.xy[2][1]:
            return False
        if not self.xy[0][0] < self.xy[1][0]:
            return False
        if not self.xy[3][0] < self.xy[2][0]:
            return False
        # sorted = self._order_points(deepcopy(self.xy))
        # sorted == self.xy
        return True

    def draw(self, drawer: ImageDraw, color=None, outline = None):
        drawer.polygon(self.xy, outline=outline, fill=color)

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        super().resize(current_dim, target_dim)
        assert self.is_sorted()

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        super().crop(current_dim, target_dim, cut_left)
        assert self.is_sorted()


class Rectangle(Polygon):
    def __init__(self, xy):
        super().__init__(xy=xy)
        assert len(xy) == 2

    def draw(self, drawer: ImageDraw, color: Tuple = None, outline = None, width = None):
        drawer.rectangle(self.xy, outline=outline, fill=color, width=width)


class Line(Polygon):
    def __init__(self, xy):
        super().__init__(xy=xy)
        assert len(xy) == 2
        assert xy[0][0] < xy[1][0]  # assert line is sorted left to right

    def draw(self, drawer: ImageDraw, outline=None, color: Tuple = None):
        if outline is None:
            warnings.warn("The Line vector object doesn't provide an outline due to it's nature. Use 'fill' to specify "
                          "the color of the line.")
        drawer.line(self.xy, fill=color)

    def get_min_x_coord(self):
        assert self.xy[0][0] < self.xy[1][0]
        return self.xy[0]

    def get_max_x_coord(self):
        assert self.xy[0][0] < self.xy[1][0]
        return self.xy[1]
