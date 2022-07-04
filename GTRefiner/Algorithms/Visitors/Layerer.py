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


class Layerer(LayoutVisitor):

    def __init__(self, vector_gt: VectorGT):
        self.px_gt: PixelLevelGT = PixelLevelGT(vector_gt.get_dim())
        self.vector_gt: VectorGT = vector_gt

    def layer(self, layout_class: Layout):
        for elem in layout_class.page_elements:
            target_layers = self._get_target_layers(page_elem=elem)
            self._draw_on_target_layers(target_layers=target_layers,page_elem=elem)

    def _get_target_layers(self, page_elem: PageElement) -> List[Layer]:
        target_classes: List[LayoutClasses] = LayoutClasses.get_layout_classes_containing(page_elem.layout_class)
        target_layers: List[Layer] = []
        for target_class in target_classes:
            target_layers.append(self.px_gt.get_layer(target_class))
        return target_layers

    @classmethod
    def _draw_on_target_layers(cls, target_layers: List[Layer], page_elem: PageElement):
        for layer in target_layers:
            layer.draw(page_elem)

    def visitMainText(self, main_text: MainText):
        self.layer(main_text)

    def visitCommentText(self, comment_text: CommentText):
        self.layer(comment_text)

    def visitDecorations(self, decorations: Decorations):
        self.layer(decorations)
