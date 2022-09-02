from GTRefiner.BuildingTools.Visitor import Visitor
from GTRefiner.GTRepresentation.Page import Page
from GTRefiner.GTRepresentation.Table import VisibilityTable


class VisibilityVisitor(Visitor):
    """ Based on a visibility table, set all elements in the vector ground-truth :class:`VectorGT` and all layers of
    the pixel level ground-truth:class:`PixelLevelGT` to the specified boolean value. Analogous to the Colorer,
    the Visibility-Visitor reads a visibility table that defines whether a layout class should be visible or not. If the
    user decides that only individual text regions or text elements are of interest, a new visitor can be written that
    implements the desired functionality.
    :param vis_table: visibility table.
    :type vis_table: VisibilityTable

    """

    def __init__(self, vis_table: VisibilityTable = None):
        """Constructor Method
        """
        self.vis_table = vis_table

    def visit_page(self, page: Page):
        """Based on a visibility table, set all elements in the vector ground-truth :class:`VectorGT` and all layers of
        the pixel level ground-truth:class:`PixelLevelGT` to the specified boolean value.
        :param page: Page that should be set visible according to the visibility table provided within the page :class:
        `Page` or can be set Visible with a custom visibility table provided by the instance (at instantiation).
        :type page: Page
        """
        if self.vis_table is not None:
            vis_table = self.vis_table
        else:
            vis_table = page.vis_table
        for region in page.vector_gt.regions:
            region.set_visible(vis_table=vis_table)
            for layout in region.text_regions:
                layout.set_visible(vis_table=vis_table)
                for elem in layout.page_elements:
                    elem.set_visible(vis_table=vis_table)
        page.px_gt.set_visible(vis_table=vis_table)
