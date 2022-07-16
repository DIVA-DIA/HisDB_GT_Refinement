from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import TextLine, \
    AscenderDescenderRegion
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import LayoutVisitor


class TextLineDecorator(LayoutVisitor):

    @classmethod
    @abstractmethod
    def decorate(cls, page: Page):
        pass


class AscenderDescenderDecorator(TextLineDecorator):

    def __init__(self, x_height: int):
        self.x_height = x_height

    def decorate(self, page: Page):
        if self.x_height is None:
            raise ValueError("provide x_height")
        for layout in page.vector_gt.regions:
            for region in layout.text_regions:
                for i, elem in enumerate(region.page_elements):
                    if isinstance(elem, TextLine):
                        region.page_elements[i] = AscenderDescenderRegion(text_line=elem, x_height=self.x_height)


class HeadAndTailDecorator(TextLineDecorator):
    pass


class HistogramDecorator(TextLineDecorator):
    pass
