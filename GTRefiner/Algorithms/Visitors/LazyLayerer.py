from abc import abstractmethod
from typing import List

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import PageElement
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT
from HisDB_GT_Refinement.GTRefiner.Algorithms.Visitor import LayoutVisitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import Decorations, CommentText, \
    MainText, Layout

# Layerer successfully draws maintext, comments and decorations on the px_gt. However, it's difficult for the layerer to
# get to decorators. Thus I will implement a layer method (like the draw) for every leaf of PageElements. This way I
# won't have to care about traversing the the tree structure.


class Layerer(LayoutVisitor):

    def __init__(self, vector_gt: VectorGT):
        self.px_gt: PixelLevelGT = PixelLevelGT(vector_gt.get_dim())
        self.vector_gt: VectorGT = vector_gt

    def layer(self, layout_class: Layout):
        for elem in layout_class.page_elements:
            elem.layer(self.px_gt)

    def visitMainText(self, main_text: MainText):
        self.layer(main_text)

    def visitCommentText(self, comment_text: CommentText):
        self.layer(comment_text)

    def visitDecorations(self, decorations: Decorations):
        self.layer(decorations)
