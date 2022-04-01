from typing import Tuple, List

from PIL import ImageDraw

from HisDB_GT_Refinement.prototype_03.Classes.NewOOP import MyPolygon
from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.Scalable import Scalable

# TODO implement draw and resize
# TODO: Problem: sepcify color and fill for polygons boundary boxes, etc.
#  Implement two interfaces: Drawable (draw method) interface and Scalable (scale) interface
#  Implement the Command design pattern so the Drawable interface doesn't have to implement two different draw methods.
class TextLine(Scalable):

    outline = (255,255,255)
    fill = False

    def __init__(self, polygon: MyPolygon.Polygon):
        self.polygon: MyPolygon.Polygon = polygon
        self.boundary_box: MyPolygon.BoundaryBox = self.polygon.boundary_box

    def draw(self, drawer: ImageDraw):
        self.polygon.draw(drawer)
        self.boundary_box.draw(drawer)

    def resize(self, size: Tuple):
        pass

# Main-Text hat ein Polygon vom xml,
# eine baseline vom xml (später dann vielleicht eine eigene)
# eine boundary box, welche ich generiere
class MainTextLine(TextLine):

    def __init__(self, polygon, baseline):
        super().__init__(polygon)
        self.baseline = baseline

# Comment hat ein Polygon vom xml,
# eine baseline vom xml (später dann vielleicht eine eigene)
# eine boundary box, welche ich generieren könnte, welche aber auch als TextRegion im xml gespeichert ist.
# TODO: test if boundary_box (generated yourself) and text_region from the xml are equal
class CommentLine(TextLine):
    # Assumption: Text_Region of Comments are equal to their boundary boxes.
    def __init__(self, polygon, baseline):
        super().__init__(polygon)
        self.baseline = baseline

# Decoration sind im xml als text-region gespeichert, dabei ist es einfach ein polygon (und nicht wirklich eine region)
class DecorationElement(TextLine):
    def __init__(self, polygon):
        super().__init__(polygon)


# Diese Klasse soll die maintext_linien einer seite als solche speichern. Des weiteren soll die information enthalten sein,
# wie deise dargestellt werden soll

# TODO implement draw & scale

class Text(Scalable):

    def __init__(self, text_lines : List[TextLine] = None):
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

    def __init__(self, main_text_lines : List[MainTextLine] = None):
        super().__init__(main_text_lines)

class CommentText(Text):

    def __init__(self, comments: List[CommentLine] = None):
        super().__init__(comments)

class Decorations(Text):

    def __init__(self, decorations: List[DecorationElement] = None):
        super().__init__(decorations)







