from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import VectorGT
from HisDB_GT_Refinement.GTRefiner.Algorithms.Visitor import LayoutVisitor


class TextLineDecorator(LayoutVisitor):

    @abstractmethod
    def __init__(self, vector_gt: VectorGT):
        self.vector_gt: VectorGT = vector_gt

class AscenderDescenderDecorator(TextLineDecorator):
    pass

class HeadAndTailDecorator(TextLineDecorator):
    pass

class HistogramDecorator(TextLineDecorator):
    pass

