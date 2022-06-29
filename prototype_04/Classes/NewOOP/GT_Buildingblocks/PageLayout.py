from typing import List, Tuple

from PIL.ImageDraw import ImageDraw

from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.GT_Buildingblocks.ImageDimension import ImageDimension
from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.GT_Buildingblocks.PageElements import PageElement, MainTextLine, \
    CommentLine, DecorationElement, TextRegionElement
from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.Interfaces.Scalable import Scalable


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