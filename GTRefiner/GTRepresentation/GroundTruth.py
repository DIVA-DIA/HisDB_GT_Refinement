from abc import abstractmethod

from GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Scalable,Showable, Croppable


class GroundTruth(Scalable, Showable, Croppable):
    """ GroundTruth is an abstract class that provides the provides the common interface for ground-truth classes.
    """

    @abstractmethod
    def __init__(self,img_dim: ImageDimension):
        self.img_dim = img_dim

    def get_dim(self):
        """ Get the ground truth's dimension.
        :return: dimension of the ground truth.
        :rtype: ImageDimension
        """
        return self.img_dim

    @abstractmethod
    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        """Resizes all ground-truth information of the current :class: `LayoutClass` to a given target
        dimension.
        :param current_dim: Current dimension
        :type current_dim: ImageDimension
        :param target_dim: Target dimension
        :type target_dim: ImageDimension
        """
        pass

    @abstractmethod
    def show(self):
        """Illustrate the ground truth."""
        pass

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        """Crop all ground truth information of this ground truth to a target dimension. Due to the nature of the ground
        truth document.
        :param cut_left: must be provided.
        :param current_dim: Current dimension
        :type current_dim: ImageDimension
        :param target_dim: Target dimension
        :type target_dim: ImageDimension
        :param cut_left: Whether or not the page is cut_left or not.
        :type cut_left: bool
        """
        pass




