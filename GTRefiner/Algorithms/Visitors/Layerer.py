from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import PixelLevelGT, VectorGT
from HisDB_GT_Refinement.GTRefiner.Algorithms.Visitor import LayoutVisitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import Decorations, CommentText, \
    MainText


class Layerer():

    def __init__(self, px_gt: PixelLevelGT, vector_gt: VectorGT):
        self.px_gt: PixelLevelGT = px_gt
        self.vector_gt: VectorGT = vector_gt

    def layer(self):
        for layout_class, region in self.vector_gt.regions:
            layer: Layer = region[LayoutClasses]




