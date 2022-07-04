from __future__ import annotations
from typing import List
import warnings

from PIL import ImageDraw

# from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import PixelLevelGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import *
# from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.Layarable import Layarable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
# from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import PageElement, \
    MainTextLine, CommentTextLine, DecorationElement
#from HisDB_GT_Refinement.GTRefiner.Algorithms.Visitor import LayoutVisitor


class Layout(Scalable, Drawable, Croppable):

    @abstractmethod
    def __init__(self):
        self.page_elements: List[PageElement] = []
        self.layout_class: List[LayoutClasses] = []
        self.color: Tuple = (255, 255, 255)
        self.is_visible: bool = True

    @abstractmethod
    def accept_layout_visitor(self, visitor):
        pass

    def set_color(self, color: Tuple):
        self.color = color

    def set_is_visible(self, is_visible: bool):
        self.is_visible = is_visible

    def add_elem(self, elem: PageElement):
        self.page_elements.append(elem)
        self.layout_class.append(elem.layout_class)

    def split(self, elem: PageElement):
        pass

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        for elem in self.page_elements:
            elem.resize(current_dim=current_dim, target_dim=target_dim)

    # def layer(self, px_gt: PixelLevelGT):
    #     for layout_class in self.layout_class:
    #         drawable_layer: Layer = px_gt.levels[layout_class]
    #         drawer = ImageDraw(drawable_layer.img_from_layer())
    #         for page_element in self.page_elements:
    #             if layout_class in page_element.layout_class:
    #                 # find the target element, can be a decorator. Thus, the code is a bit more extensive.
    #                 target_element = page_element._find_layout_class
    #             page_element.set_is_filled(True)
    #             self.draw(drawer,color = (1,))
    #
    # def _find_layout_class(self, elem: PageElement, layout_class: LayoutClasses):
    #     pass

    def get_text_region(self):
        pass

    def draw(self, drawer: ImageDraw, color: Tuple = None):
        for elem in self.page_elements:
            elem.draw(drawer=drawer, color=color)

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        for elem in self.page_elements:
            elem.crop(current_dim=current_dim, target_dim=target_dim, cut_left=cut_left)


class MainText(Layout):
    @abstractmethod
    def __init__(self):
        super().__init__()
        self.page_elements: List[MainTextLine] = []
        self.layout_class.append(LayoutClasses.MAINTEXT)

    def accept_layout_visitor(self, visitor):
        visitor.visitMainText(self)


class CommentText(Layout):
    @abstractmethod
    def __init__(self):
        super().__init__()
        self.page_elements: List[CommentTextLine] = []
        self.layout_class.append(LayoutClasses.COMMENT)

    def accept_layout_visitor(self, visitor):
        visitor.visitCommentText(self)


class Decorations(Layout):
    @abstractmethod
    def __init__(self):
        super().__init__()
        self.page_elements: List[DecorationElement] = []
        self.layout_class.append(LayoutClasses.DECORATION)

    def accept_layout_visitor(self, visitor):
        visitor.visitDecorations(self)


class TextRegion(Layout):

    def __init__(self, layout: Layout):
        super().__init__()
        self.text_regions: List[Layout] = []
        self.add_region(layout)

    def add_region(self, layout: Layout):
        if isinstance(layout, TextRegion):
            raise AttributeError("You're adding a text region in this text region. Use the merge() to do so.")
        self.text_regions.append(layout)

    def merge(self, other: TextRegion):
        pass

    def accept_layout_visitor(self, visitor):
        for layout in self.text_regions:
            layout.accept_layout_visitor(visitor)
