from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import VectorGT, PixelLevelGT
from HisDB_GT_Refinement.GTRefiner.Algorithms.Visitor import LayoutVisitor


class Colorer(LayoutVisitor):
    """
    Sets the colors of the vector objects and the different levels of the pixel groundtruth.
    """

    @abstractmethod
    def __init__(self, vector_gt: VectorGT, px_gt: PixelLevelGT ):
        self.vector_gt: VectorGT = vector_gt
        self.px_gt: PixelLevelGT = px_gt

class UniColor(Colorer):
    pass

class AlternatingTextLine(Colorer):
    pass

class AscenderDescenderColorer(Colorer):
    pass