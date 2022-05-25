import operator
from typing import Tuple, List

from PIL import ImageDraw

from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.Scalable import Scalable
from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.VectorObject import Polygon, BoundingBox, Line, XRegion
from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.ImageDimension import ImageDimension

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
        self.fill = None # no fill by default
        self.polygon: Polygon = polygon
        self.boundary_box: BoundingBox = BoundingBox(polygon=polygon)

    def draw(self, drawer: ImageDraw):
        self.polygon.draw(drawer=drawer,outline=self.outline, fill=self.fill)
        self.boundary_box.draw(drawer, outline=self.outline, fill=self.fill)

    def resize(self, scale_factor: Tuple[float,float]):
        self.polygon.resize(scale_factor)
        self.boundary_box.resize(scale_factor)

    def crop(self, source_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        self.polygon.crop(source_dim=source_dim, target_dim=target_dim,cut_left=cut_left)
        self.boundary_box = BoundingBox(polygon=self.polygon)

    def is_filled(self):
        return self.fill is None

    def set_fill(self, fill: Tuple[int,int,int]):
        self.fill = fill

class TextLine(PageElement):
    def __init__(self, polygon: Polygon, baseline: Line):
        super().__init__(polygon)
        self.xRegion: XRegion = XRegion(baseline, self.boundary_box)

    def draw(self, drawer: ImageDraw):
        self.xRegion.draw(drawer=drawer, outline=self.outline)
        super().draw(drawer)

    def resize(self, scale_factor: Tuple[float,float]):
        super(TextLine, self).resize(scale_factor=scale_factor)
        self.xRegion.resize(scale_factor=scale_factor)

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
# TODO: test if boundary_box (generated yourself) and text_region from the xml are equal
class CommentLine(TextLine):

    # Assumption: Text_Region of Comments are equal to their boundary boxes.
    def __init__(self, polygon: Polygon, baseline: Line):
        super().__init__(polygon,baseline)
        self.outline = (0, 255, 0)  # green

# Decoration sind im xml als text-region gespeichert, dabei ist es einfach ein polygon (und nicht wirklich eine region)
class DecorationElement(PageElement):

    def __init__(self, polygon: Polygon):
        super().__init__(polygon)
        self.outline = (0, 0, 255)  # blue

class TextRegionElement(PageElement):

    def __init__(self, rectangle: Polygon, color = (255, 0, 255)):
        super().__init__(polygon=rectangle)
        self.outline = color   # purple






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

    def resize(self, scale_factor: Tuple[float,float]):
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



