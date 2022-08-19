from typing import List, Tuple
from abc import abstractmethod
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import Visitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import ColorTable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import PageElement


class Colorer(Visitor):
    """ Default implementation of Colorer sets the colors of the vector objects and the different levels of the pixel
        ground truth
        :param color_table: colors of color table are used to define the colors of the differenet page
        elements :class:`PageElement`, layouts :class:`Layout` and regions, :class:`Region`.
        :type color_table: ColorTable
    """

    def __init__(self, color_table: ColorTable = None):
        """ Constructor method
        """
        self.color_table = color_table

    def visit_page(self, page: Page):
        """
        Set the colors of the ground truth information from page. Supported strategies are alternating, all the same,
        all different or any other combination of colors given in the color table. This Colorer just iterates over the
        colors given.
        :param page: Is going to be colored according to the color table from the instance of self
        :type page: Page
        """
        if self.color_table is not None:
            col_table = self.color_table
        else:
            col_table = page.col_table
        # set color for vector_gt
        for region in page.vector_gt.regions:
            region.set_color(color_table=col_table)
            for layout in region.text_regions:
                layout.set_color(color_table=col_table)
                for elem in layout.page_elements:
                    elem.set_color(color_table=col_table)
        # set color for px_gt
        page.px_gt.set_color(color_table=col_table)
