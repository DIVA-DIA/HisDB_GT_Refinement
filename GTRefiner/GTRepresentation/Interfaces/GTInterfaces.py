from abc import abstractmethod
from typing import Tuple, Dict
from PIL.ImageDraw import ImageDraw

from GTRefiner.GTRepresentation.ImageDimension import ImageDimension


class Scalable():

    @abstractmethod
    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        """Introduces the behaviour of a scalable object. Based on a current dimension and a target dimension the object
        implementing this behaviour should be able to scale to the target dimension.
        :param current_dim: Current dimension
        :type current_dim: ImageDimension
        :param target_dim: Target dimension
        :type target_dim: ImageDimension
        """
        pass


class Croppable():

    @abstractmethod
    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        """Introduces the behaviour of a croppable object. Based on a current dimension and a target dimension the object
        implementing this behaviour should be able to be cropped to the target dimension.
        :param current_dim: Current dimension
        :type current_dim: ImageDimension
        :param target_dim: Target dimension
        :type target_dim: ImageDimension
        """
        pass


class Drawable:

    @abstractmethod
    def draw(self, drawer: ImageDraw, color: Tuple = None, outline=None):
        """ Draw the vector object or collection of vector_objects. Useful for drawing on :class: `Layer`, for debugging
        purposes, and used by the :class: `Showable` interface."""


class Showable():

    @abstractmethod
    def show(self):
        """ Draw the vector object or collection of vector_objects and show them on an Pillow Image. Useful to debug and
        make sure that the program is doing what it's supposed to. Closely related to the :class: `Showable` interface.
        """
        pass


class Dictionable():

    @abstractmethod
    def build(self) -> Dict:
        """Introduces the behaviour of a JSON compliant represenation. The returned dictionary is supposed to be stored
        in a JSON file.
        :return: Dictionary of all the vector objects of interest.
        :rtype: dict
        """
        pass
