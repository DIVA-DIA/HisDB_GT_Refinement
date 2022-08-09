from typing import List, Tuple
from abc import abstractmethod
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import Visitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import ColorTable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import PageElement


class Colorer(Visitor):
    """
    Sets the colors of the vector objects and the different levels of the pixel groundtruth.
    """
    def __init__(self, color_table: ColorTable = None):
        self.color_table = color_table

    def visit_page(self, page: Page):
        if self.color_table is not None:
            col_table = self.color_table
        else:
            col_table = page.col_table
        for region in page.vector_gt.regions:
            for layout in region.text_regions:
                for elem in layout.page_elements:
                    elem.set_color(color_table=col_table)
        page.px_gt.set_color(color_table=col_table)


# class ColoringStrategy:
#
#     @abstractmethod
#     def color(self, page_elem: PageElement, color_table: ColorTable):
#         pass
#
# class UniColorStrategy(ColoringStrategy):
#
#     def color(self, page_elem: PageElement, color_table: ColorTable):
#         page_elem = page_elem.set_color(color_table[page_elem.layout_class])
#
# class AlternatingStrategy(ColoringStrategy):
#
#     def color(self, page_elem: PageElement, color_table: ColorTable):
#         page_elem = page_elem.set_color(color_table[page_elem.layout_class])

#
# class AlternatingTextLine(Colorer):
#     """
#     Alternates colors of the textlines. For now it only supports MainText, Comments, Decorations.
#     """
#
#     def __init__(self, target_class: LayoutClasses):
#         if target_class is not LayoutClasses.MAINTEXT or target_class is not LayoutClasses.COMMENT or target_class is not LayoutClasses.DECORATION:
#             raise AttributeError(f"{target_class.name} not supported")
#         self.target_class = target_class
#
#     def visit_page(self, page: Page):
#         root_col = page.col_table[self.target_class]
#         reserved_colors = self._get_reserved_colors(page)
#         for region in page.vector_gt.regions:
#             for layout in region.text_regions:
#                 for i, elem in enumerate(layout.page_elements):
#                     if elem.layout_class == self.target_class:
#                         elem.set_color(color_table=page.col_table)
#         page.px_gt.set_color(color_table=page.col_table)
#
#     def _get_reserved_colors(self, page):
#         """ Returns unique colors of base classes (MainText, Comments, Decoration) and """
#         colors: List[Tuple] = []
#         # reserve all colors from the color table
#         for l_class in LayoutClasses:
#             if l_class.value not in colors:
#                 colors.append(l_class.value)
#         # reserve all
#         for region in page.vector_gt.regions:
#             for layout in region.text_regions:
#                 for i, elem in enumerate(layout.page_elements):
#                     if elem.get_color not in colors:
#                         colors.append(elem.get_color())  # get unique colors
#         return colors
#
#
# class AscenderDescenderColorer(Colorer):
#     pass
