import operator
from typing import Tuple, List

from PIL import ImageDraw

from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.Interfaces.Scalable import Scalable
from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.GT_Buildingblocks.VectorObject import Polygon, BoundingBox, Line, Box
from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.GT_Buildingblocks.ImageDimension import ImageDimension

OFFSET = 50


# TODO implement resize
# TODO: Problem: sepcify color and fill for polygons boundary boxes, etc.
#  Implement two interfaces: Drawable (draw method) interface and Scalable (scale) interface
#  Implement the Command design pattern so the Drawable interface doesn't have to implement two different draw methods.
# TODO: convert baseline to function -> instead of (x1,y1)(x2,y2) -> y = x*m + q
class PageElement(Scalable):
    # TextObject bildet alles ab, was ein VektorGroundTruth beinhalten kann.
    def __init__(self, polygon: Polygon):
        self.outline = (255, 255, 255)  # white by default
        self.fill = None  # no fill by default
        self.polygon: Polygon = polygon
        self.boundary_box: BoundingBox = BoundingBox(polygon=polygon)

    def draw(self, drawer: ImageDraw):
        self.polygon.draw(drawer=drawer, outline=self.outline, fill=self.fill)
        self.boundary_box.draw(drawer, outline=self.outline, fill=self.fill)

    def resize(self, scale_factor: Tuple[float, float]):
        self.polygon.resize(scale_factor)
        self.boundary_box.resize(scale_factor)

    def crop(self, source_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        self.polygon.crop(source_dim=source_dim, target_dim=target_dim, cut_left=cut_left)
        self.boundary_box = BoundingBox(polygon=self.polygon)

    def is_filled(self):
        return self.fill is None

    def set_fill(self, fill: Tuple[int, int, int]):
        self.fill = fill


class TextLine(PageElement):
    def __init__(self, polygon: Polygon, baseline: Line):
        super().__init__(polygon)
        self.text_line_regions: TextlineRegions = TextlineRegions(baseline, self.boundary_box)

    def draw(self, drawer: ImageDraw):
        self.text_line_regions.draw(drawer=drawer, outline=self.outline)
        super().draw(drawer)

    def resize(self, scale_factor: Tuple[float, float]):
        super(TextLine, self).resize(scale_factor=scale_factor)
        self.text_line_regions.resize(scale_factor=scale_factor)


# Main-Text hat ein Polygon vom xml,
# eine baseline vom xml (später dann vielleicht eine eigene)
# eine boundary box, welche ich generiere
class MainTextLine(TextLine):
    def __init__(self, polygon: Polygon, baseline: Line):
        super().__init__(polygon, baseline)
        self.outline = (255, 0, 0)  # red


# Comment hat ein Polygon vom xml,
# eine baseline vom xml (später dann vielleicht eine eigene)
# eine boundary box, welche ich generieren könnte, welche aber auch als TextRegion im xml gespeichert ist.
class CommentLine(TextLine):

    # Assumption: Text_Region of Comments are equal to their boundary boxes.
    def __init__(self, polygon: Polygon, baseline: Line):
        super().__init__(polygon, baseline)
        self.outline = (0, 255, 0)  # green


# Decoration sind im xml als text-region gespeichert, dabei ist es einfach ein polygon (und nicht wirklich eine region)
class DecorationElement(PageElement):

    def __init__(self, polygon: Polygon):
        super().__init__(polygon)
        self.outline = (0, 0, 255)  # blue


class TextRegionElement(PageElement):

    def __init__(self, rectangle: Polygon, color=(255, 0, 255)):
        super().__init__(polygon=rectangle)
        self.outline = color  # purple


# Diese Klasse soll die maintext_linien einer seite als solche speichern. Des weiteren soll die information enthalten sein,
# wie deise dargestellt werden soll

# TODO implement draw & scale

class Layout(Scalable):

    def __init__(self, text_lines: List[PageElement] = None):
        if text_lines is None:
            self.text_lines: List[PageElement] = []
        else:
            self.text_lines = text_lines

    def append_elem(self, elem: PageElement):
        self.text_lines.append(elem)

    def length(self):
        return len(self.text_lines)

    def resize(self, scale_factor: Tuple[float, float]):
        for element in self.text_lines:
            element.resize(scale_factor)

    def draw(self, drawer: ImageDraw):
        for elem in self.text_lines:
            elem.draw(drawer)

    def crop(self, source_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        for elem in self.text_lines:
            elem.crop(source_dim=source_dim, target_dim=target_dim, cut_left=cut_left)

    def __getitem__(self, index):
        return self.text_lines[index]


class MainText(Layout):

    def __init__(self, main_text_lines: List[MainTextLine] = None):
        super().__init__(main_text_lines)


class CommentText(Layout):

    def __init__(self, comments: List[CommentLine] = None):
        super().__init__(comments)


class Decorations(Layout):

    def __init__(self, decorations: List[DecorationElement] = None):
        super().__init__(decorations)


class TextRegions(Layout):

    def __init__(self, text_regions: List[TextRegionElement] = None):
        super().__init__(text_regions)


# storing multiple VectorObjects.
class TextlineRegions(Scalable):
    # TODO: Integrate these regions directly into the VectorOcject: Textline. Every textline has a x_region, ascender...
    # note that the x region always intersects perfectly with the bounding_box because they share the same max_x and min_x

    def __init__(self, baseline: Line, bbox: BoundingBox, x_hight=45):
        self.x_hight = x_hight
        self.boundingbox: BoundingBox = bbox
        self.baseline: Line = baseline  # [(x1,y1),(x2,y2)]
        self.topline: Line = self._set_topline()  # [(x3,y3),(x4,y4)]
        self.x_region = self._set_x_region()  # [[(x1,y1),(x2,y2)][(x3,y3),(x4,y4)]]
        self.ascender_region = self._set_ascender_region()
        self.descender_region = self._set_descender_region()
        # super().__init__(self.x_region.xy) # TODO: Noch nicht gut implementiert.
        # Diese klasse macht noch gerade herzlich wenig sinn

    def _set_topline(self):
        return Line([tuple((x, y - self.x_hight)) for x, y in self.baseline])

    def _set_x_region(self):
        sorted_baseline = [self.baseline.xy[1], self.baseline.xy[0]]
        topline = self.topline.xy
        concatenated = topline + sorted_baseline
        return Box(concatenated)

    def _set_ascender_region(self):
        min_x = self.boundingbox.get_min_x()
        min_y = self.boundingbox.get_min_y()
        max_x = self.boundingbox.get_max_x()
        region = Box([(min_x, min_y),  # left top corner
                      (max_x, min_y),  # right top corner
                      (self.topline.get_max_x_coord()),  # right bottom corner
                      (self.topline.get_min_x_coord())  # left bottom corner
                      ])
        return region

    def _set_descender_region(self):
        min_x = self.boundingbox.get_min_x()
        max_x = self.boundingbox.get_max_x()
        max_y = self.boundingbox.get_max_y()
        region = Box([(self.baseline.get_min_x_coord()),  # left top corner
                      (self.baseline.get_max_x_coord()),  # right top corner
                      (max_x, max_y),  # right bottom corner
                      (min_x, max_y)  # left bottom corner
                      ])
        return region

    def draw(self, drawer: ImageDraw, outline=(0, 125, 255), fill=None):
        drawer.polygon(xy=self.boundingbox.xy,
                       outline=outline)
        drawer.polygon(xy=self.ascender_region.xy, outline=(125, 125, 255), fill=None)
        drawer.polygon(xy=self.descender_region.xy, outline=(125, 170, 255), fill=None)
        drawer.polygon(xy=self.x_region.xy, outline=(125, 155, 255), fill=None)

    def resize(self, scale_factor: Tuple[float, float]):
        self.x_hight = round(operator.truediv(self.x_hight, scale_factor[1]))
        # self.boundingbox.resize(scale_factor) -> wurde schon reskaliert! nicht noch einmal reskalieren :)
        self.baseline.resize(scale_factor)
        self.topline.resize(scale_factor)
        self.x_region.resize(scale_factor)
        self.ascender_region.resize(scale_factor)
        self.descender_region.resize(scale_factor)
