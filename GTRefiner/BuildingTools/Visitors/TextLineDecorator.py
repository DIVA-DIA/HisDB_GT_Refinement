from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import TextLine, \
    AscenderDescenderRegion
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import LayoutVisitor


class TextLineDecorator(LayoutVisitor):

    @classmethod
    @abstractmethod
    def decorate(cls, vector_gt: VectorGT):
        pass


class AscenderDescenderDecorator(TextLineDecorator):

    @classmethod
    def decorate(cls, vector_gt: VectorGT, x_height: int = None):
        # Not nice could be solved using **kwargs
        if x_height is None:
            raise ValueError("provide x_height")
        for layout in vector_gt.regions:
            for region in layout.text_regions:
                for i, elem in enumerate(region.page_elements):
                    if isinstance(elem, TextLine):
                        region.page_elements[i] = AscenderDescenderRegion(text_line=elem, x_height=x_height)


class HeadAndTailDecorator(TextLineDecorator):
    pass


class HistogramDecorator(TextLineDecorator):
    pass
