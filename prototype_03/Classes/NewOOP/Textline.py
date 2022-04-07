from typing import Tuple, List

from PIL import ImageDraw

from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.Scalable import Scalable
from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.VectorObject import Polygon, BoundingBox, Line, XRegion

OFFSET = 50
# TODO implement resize
# TODO: Problem: sepcify color and fill for polygons boundary boxes, etc.
#  Implement two interfaces: Drawable (draw method) interface and Scalable (scale) interface
#  Implement the Command design pattern so the Drawable interface doesn't have to implement two different draw methods.
# TODO: convert baseline to function -> instead of (x1,y1)(x2,y2) -> y = x*m + q
class TextLine(Scalable):

    def __init__(self, polygon: Polygon):
        self.outline = (255, 255, 255)  # white by default
        self.fill = None # no fill by default
        self.is_filled = False
        self.polygon: Polygon = polygon
        self.boundary_box: BoundingBox = BoundingBox(polygon=polygon)

    def draw(self, drawer: ImageDraw):
        self.polygon.draw(drawer=drawer,outline=self.outline, fill=self.fill)
        self.boundary_box.draw(drawer, outline=self.outline, fill=self.fill)

    def resize(self, size: Tuple):
        pass

    def is_filled(self):
        return self.is_filled

    def set_fill(self):
        self.fill = self.outline
        self.is_filled = True

# Main-Text hat ein Polygon vom xml,
# eine baseline vom xml (später dann vielleicht eine eigene)
# eine boundary box, welche ich generiere
class MainTextLine(TextLine):


    def __init__(self, polygon: Polygon, baseline: Line):
        super().__init__(polygon)
        self.xRegion: XRegion = XRegion(baseline, self.boundary_box)
        self.outline = (255, 0, 0)  # red

    def draw(self, drawer: ImageDraw):
        self.xRegion.draw(drawer=drawer, outline=self.outline)
        super().draw(drawer)


# Comment hat ein Polygon vom xml,
# eine baseline vom xml (später dann vielleicht eine eigene)
# eine boundary box, welche ich generieren könnte, welche aber auch als TextRegion im xml gespeichert ist.
# TODO: test if boundary_box (generated yourself) and text_region from the xml are equal
class CommentLine(TextLine):

    # Assumption: Text_Region of Comments are equal to their boundary boxes.
    def __init__(self, polygon: Polygon, baseline: Line):
        super().__init__(polygon)
        # polygon
        # bounding_box
        # x-region
        self.xRegion: XRegion = XRegion(baseline, self.boundary_box)
        self.outline = (0, 255, 0)  # green

    def draw(self, drawer: ImageDraw):
        self.xRegion.draw(drawer=drawer, outline=self.outline)
        super().draw(drawer)

# Decoration sind im xml als text-region gespeichert, dabei ist es einfach ein polygon (und nicht wirklich eine region)
class DecorationElement(TextLine):

    def __init__(self, polygon: Polygon):
        super().__init__(polygon)
        self.outline = (0, 0, 255)  # blue

class TextRegionElement(TextLine):

    def __init__(self, rectangle: Polygon, color = (255, 0, 255)):
        super().__init__(polygon=rectangle)
        self.outline = color   # purple






# Diese Klasse soll die maintext_linien einer seite als solche speichern. Des weiteren soll die information enthalten sein,
# wie deise dargestellt werden soll

# TODO implement draw & scale

class Text(Scalable):

    def __init__(self, text_lines: List[TextLine] = None):
        if text_lines is None:
            self.text_lines: List[TextLine] = []
        else:
            self.text_lines = text_lines

    def append_elem(self, elem: TextLine):
        self.text_lines.append(elem)

    def length(self):
        return len(self.text_lines)

    def draw(self, drawer: ImageDraw):
        for elem in self.text_lines:
            elem.draw(drawer)


class MainText(Text):

    def __init__(self, main_text_lines: List[MainTextLine] = None):
        super().__init__(main_text_lines)


class CommentText(Text):

    def __init__(self, comments: List[CommentLine] = None):
        super().__init__(comments)


class Decorations(Text):

    def __init__(self, decorations: List[DecorationElement] = None):
        super().__init__(decorations)

class TextRegions(Text):

    def __init__(self, text_regions: List[TextRegionElement] = None):
        super().__init__(text_regions)



