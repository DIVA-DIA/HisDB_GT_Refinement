from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import LayoutVisitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import ColorTable


class Colorer(LayoutVisitor):
    """
    Sets the colors of the vector objects and the different levels of the pixel groundtruth.
    """
    def __init__(self, color_table: ColorTable):
        self.color_table = color_table

    # def set_colors(self, page: Page):
    #     for region in page.vector_gt.regions:
    #         for layout in region.text_regions:
    #             for elem in layout.page_elements:
    #                 elem.set_color(color_table=self.color_table)


class UniColor(Colorer):
    pass

class AlternatingTextLine(Colorer):
    pass

class AscenderDescenderColorer(Colorer):
    pass