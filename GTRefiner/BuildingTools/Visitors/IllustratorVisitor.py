import copy
from typing import Tuple

from PIL import ImageDraw, Image

from GTRefiner.BuildingTools.Visitor import Visitor
from GTRefiner.BuildingTools.Visitors.Colorer import Colorer
from GTRefiner.BuildingTools.Visitors.VisibilityVisitor import VisibilityVisitor
from GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from GTRefiner.GTRepresentation.Page import Page
from GTRefiner.GTRepresentation.Table import ColorTable, VisibilityTable


class Illustrator(Visitor):
    """Illustrator serves for visualizing processes.
    :param background: If you want the vector gt to be drawn on a background, specify the image
    :type background: Image
    :param color_table: If you want another color table than the quick and dirty specified in this class
    :type color_table: ColorTable
    :param vis_table: If you want another vis table than the quick and dirty specified in this class
    :type vis_table: VisibilityTable
    :param outline: Specify the outline color here, if None is given no outline will be drawn.
    :type outline: tuple
    """
    # quick and dirty color table
    main_text_color = [(10, 20, 255)]
    comment_color = [(255, 20, 255)]
    decoration_color = [(20, 255, 255)]

    color_table = ColorTable({LayoutClasses.MAINTEXT: main_text_color,
                              LayoutClasses.COMMENT: comment_color,
                              LayoutClasses.DECORATION: decoration_color})
    # quick and dirty visiblity table
    vis_table = VisibilityTable({LayoutClasses.MAINTEXT: False,
                                 LayoutClasses.COMMENT: True,
                                 LayoutClasses.DECORATION: False,
                                 LayoutClasses.ASCENDER: True,
                                 LayoutClasses.DESCENDER: True,
                                 LayoutClasses.TEXT_REGION: True,
                                 LayoutClasses.MAINTEXT_AND_DECORATION_AND_COMMENT: True,
                                 LayoutClasses.MAINTEXT_AND_DECORATION: True,
                                 LayoutClasses.COMMENT_AND_MAINTEXT: True,
                                 LayoutClasses.COMMENT_AND_DECORATION: True,
                                 LayoutClasses.XREGION: False,
                                 LayoutClasses.BASELINE: True,
                                 LayoutClasses.BACKGROUND: False})

    def __init__(self, background: Image = None, color_table: ColorTable = None,
                 vis_table: VisibilityTable = None, outline: Tuple = None):
        """Constructor method
        """
        self.background = background
        self.outline = outline
        if color_table is not None:
            self.color_table = color_table
        if vis_table is not None:
            self.vis_table = vis_table

    def visit_page(self, page: Page):
        """ Illustrate the page.
        :param page: page to illustrate
        :type page: Page
        :return: If a background is given its going to be blended.
        :rtype: Image
        """
        drawn_vector_objects = Image.new("RGB", page.get_img_dim().to_tuple())
        if self.background is None:
            self.background = copy.deepcopy(page.raw_img.img).convert("RGB")
        drawer = ImageDraw.Draw(drawn_vector_objects)

        page.vector_gt.draw(drawer=drawer, outline=self.outline)
        drawn_vector_objects.show()

        colorer = Colorer(self.color_table)
        colorer.visit_page(page=page)

        for region in page.vector_gt.regions:
            region._is_sorted()
        page.vector_gt.draw(drawer=drawer, outline=self.outline)
        drawn_vector_objects.show()


        visbility_visitor = VisibilityVisitor(vis_table=self.vis_table)
        visbility_visitor.visit_page(page)

        page.vector_gt.draw(drawer=drawer, outline=self.outline)
        drawn_vector_objects.show()


        page.vector_gt.show()
        page.raw_img.show()
        #page.px_gt.show()
        if self.background is None:
            return drawn_vector_objects
        return Image.blend(drawn_vector_objects, self.background, 0.5)
