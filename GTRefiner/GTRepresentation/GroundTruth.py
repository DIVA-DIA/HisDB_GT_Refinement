from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Scalable,Showable, Croppable


class GroundTruth(Scalable, Showable, Croppable):
    """ GroundTruth is an abstract class that provides the provides the

    """

    @abstractmethod
    def __init__(self,img_dim: ImageDimension):
        self.img_dim = img_dim

    def get_dim(self):
        return self.img_dim

    @abstractmethod
    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        pass

    @abstractmethod
    def show(self):
        pass


