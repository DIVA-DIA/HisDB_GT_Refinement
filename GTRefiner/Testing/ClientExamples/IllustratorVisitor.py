from PIL import ImageDraw, Image
import copy

from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import Visitor
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Colorer import Colorer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import ColorTable


class Illustrator(Visitor):

    main_text_color = [(10,20,255)]
    comment_color = (255,20,255)
    decoration_color = (20, 255, 255)

    color_table = ColorTable({LayoutClasses.MAINTEXT: main_text_color,
                              LayoutClasses.COMMENT: [comment_color],
                              LayoutClasses.DECORATION: [decoration_color]})

    def __init__(self, background: Image = None):
        self.background = background

    def visit_page(self, page: Page):
        drawn_vector_objects = Image.new("RGB", page.get_img_dim().to_tuple())
        if self.background is None:
            self.background = copy.deepcopy(page.raw_img.img).convert("RGB")
        drawer = ImageDraw.Draw(drawn_vector_objects)
        colorer = Colorer(self.color_table)
        colorer.visit_page(page=page)
        page.vector_gt.draw(drawer=drawer)
        page.vector_gt.show()
        page.raw_img.show()
        page.px_gt.show()
        return Image.blend(drawn_vector_objects,self.background,0.5)



