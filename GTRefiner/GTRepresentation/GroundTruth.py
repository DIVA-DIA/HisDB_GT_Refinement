from abc import abstractmethod
from typing import Dict, List

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Scalable,Showable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import TextRegion


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

    def __init__(self, regions: Dict[LayoutClasses, List[TextRegion]]):
        self.regions: Dict[LayoutClasses, List[TextRegion]] = regions


class MyImage(GroundTruth):
    pass


class PixelLevelGT(MyImage):

    def __init__(self):
        self.levels: Dict[LayoutClasses, Layer] = self._initialize_empty_px_gt()

    def _initialize_empty_px_gt(self) -> Dict[LayoutClasses, List[Layer]]:
        pass


class RawImage(MyImage):
    pass



