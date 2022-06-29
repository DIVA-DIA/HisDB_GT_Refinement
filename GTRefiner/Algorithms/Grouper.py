from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import VectorGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses


class Grouper:

    @abstractmethod
    def __init__(self, vector_gt: VectorGT):
        self.vector_gt = vector_gt


class ParagraphGrouper(Grouper):

    def __init__(self, vector_gt: VectorGT, LayoutClass: LayoutClasses):
        super().__init__(vector_gt)
        pass

