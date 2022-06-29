from abc import abstractmethod
from typing import Dict, List

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GTInterfaces import Scalable,Showable



class GroundTruth(Scalable, Showable):
    """ GroundTruth is an abstract class that provides the provides the

    """

    @abstractmethod
    def init(self, img_dim: ImageDimension):
        self.img_dim = img_dim

    def get_dim(self):
        return self.img_dim

    @abstractmethod
    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        pass

    @abstractmethod
    def show(self):
        pass


class VectorGT(GroundTruth):
    pass


class MyImage(GroundTruth):
    pass


class PixelLevelGT(MyImage):
    pass


class RawImage(MyImage):
    pass



