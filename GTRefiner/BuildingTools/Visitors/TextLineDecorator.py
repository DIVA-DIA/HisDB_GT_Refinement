from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import Visitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import TextLine, \
    AscenderDescenderRegion


class TextLineDecorator(Visitor):

    @classmethod
    @abstractmethod
    def visit_page(self, page: Page):
        """Decorate textline elements of page."""
        pass


class AscenderDescenderDecorator(TextLineDecorator):
    """
    :param x_height: Based on this int value and a baseline provided by the TextLine element calculate Ascenders,
    Descenders and x-Height (Rectangles).
    :type x_height: int
    """

    def __init__(self, x_height: int):
        """Constructor method
        """
        self.x_height = x_height

    def visit_page(self, page: Page):
        """Decorate all TextLine instaces elements of page."""
        if self.x_height is None:
            raise ValueError("provide x_height")
        for layout in page.vector_gt.regions:
            for region in layout.text_regions:
                for i, elem in enumerate(region.page_elements):
                    if isinstance(elem, TextLine):
                        region.page_elements[i] = AscenderDescenderRegion(text_line=elem, x_height=self.x_height)


class HeadAndTailDecorator(TextLineDecorator):
    """
        "Example of another Decorator Class"
    """

    pass


class HistogramDecorator(TextLineDecorator):
    """
        "Example of another Decorator Class"
    """
    pass
