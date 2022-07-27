from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import Visitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page


class VisibilityVisitor(Visitor):

    def visit_page(self, page: Page):
        for region in page.vector_gt.regions:
            for layout in region.text_regions:
                for elem in layout.page_elements:
                    elem.set_visible(vis_table=page.vis_table)
        page.px_gt.set_visible(vis_table=page.vis_table)