from abc import abstractmethod
from typing import Tuple
from PIL.ImageDraw import ImageDraw

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension


class Scalable():

    @abstractmethod
    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        pass


class Layarable:

    @abstractmethod
    def layer(self):
        pass


class Drawable:

    @abstractmethod
    def draw(self, drawer: ImageDraw, color: Tuple = None, is_filled: bool = None):
        pass


class Showable():

    @abstractmethod
    def show(self):
        pass


class Croppable():

    @abstractmethod
    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        pass
