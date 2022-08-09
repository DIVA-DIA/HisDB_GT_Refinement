from abc import abstractmethod
from typing import Tuple, Dict
from PIL.ImageDraw import ImageDraw

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension


class Scalable():

    @abstractmethod
    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        pass


class Croppable():

    @abstractmethod
    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        pass


class Drawable:

    @abstractmethod
    def draw(self, drawer: ImageDraw, color: Tuple = None, outline = None):
        """ Draw the vector object or collection of vector_objects. Useful for drawing on :class: `Layer`, for debugging
        purposes, and used by the :class: `Showable interface."""


class Showable():

    @abstractmethod
    def show(self):
        # TODO: Redundant class. Depends on the draw function. Delete it and its implementations in subclasses.
        pass


class Dictionable():

    @abstractmethod
    def build(self) -> Dict:
        pass
