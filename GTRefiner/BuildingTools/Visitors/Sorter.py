from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import Visitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page


class Sorter(Visitor):
    """
    Sort a given container of objects.
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
