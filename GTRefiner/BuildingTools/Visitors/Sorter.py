from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import Visitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page


class Sorter(Visitor):
    """
    Sort a given container of objects. The text elements of the vectorized ground truth of the DIVA-HisDB are not
    consistently sorted, which is why the Sorter should always be used if the order of the text elements matters.
    We implement this function by having the layout and TextRegion classes both override __lt__() base-function of the
    Python object. Thus they provide an interface for efficient sorting (thanks to Python's built-in sorting algorithms)
    of text elements and regions. The sorter tool can be used to invoke, add to, and modify this behavior as desired.
    The sorter goes hand in hand with the grouper tool, see module Grouper, and the alternating colorer, see module
    Colorer.
    """

    @abstractmethod
    def visit_page(self, page: Page):
        pass


class DescendingSorter(Sorter):

    def visit_page(self, page: Page):
        """Sort all elems of a region in descending order (descending = highest y value first).
        :param page: page to be sorted.
        :type page: Page
        """
        for region in page.vector_gt.regions:
            region.sort_layout_elements(reverse=False)


class AscendingSorter(Sorter):

    def visit_page(self, page: Page):
        """Sort all elems of a region in ascending order (ascending = lowest y value first).
        :param page: page to be sorted.
        :type page: Page
        """
        for region in page.vector_gt.regions:
            region.sort_layout_elements(reverse=True)
