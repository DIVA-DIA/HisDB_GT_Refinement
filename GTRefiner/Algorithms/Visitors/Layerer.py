from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import PixelLevelGT
from HisDB_GT_Refinement.GTRefiner.Algorithms.Visitor import LayoutVisitor


class TextLineDecorator(LayoutVisitor):

    def __init__(self, px_gt: PixelLevelGT):
        self.px_gt: PixelLevelGT = px_gt

