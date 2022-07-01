from typing import List

from PIL import ImageDraw

from HisDB_GT_Refinement.GTRefiner.Algorithms.Visitor import LayoutVisitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import PixelLevelGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import *
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.Layarable import Layarable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import PageElement, MainTextLine


class Layout(Layarable, Scalable, Drawable, Croppable):

    @abstractmethod
    def __init__(self):
        self.page_elements: List[PageElement] = []
        self.layout_class: List[LayoutClasses] = []
        self.color: Tuple = (255,255,255)
        self.is_visible = True

    @abstractmethod
    def accept_layout_visitor(self, visitor: LayoutVisitor):
        pass

    def set_color(self, color: Tuple):
        self.color = color

    def set_is_visible(self, is_visible: bool):
        self.is_visible = is_visible

    def add_elem(self, elem: PageElement):
        self.page_elements.append(elem)
        self.layout_class.extend(elem.layout_class)

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        for elem in self.page_elements:
            elem.resize(current_dim=current_dim,target_dim=target_dim)

    def layer(self, px_gt: PixelLevelGT):
        for layout_class in self.layout_class:
            drawable_layer: Layer = px_gt.levels[layout_class]
            drawer = ImageDraw(drawable_layer.img_from_layer())
            self.draw(drawer,color = tuple(1))

    def draw(self, drawer: ImageDraw, color: Tuple = None):
        for elem in self.page_elements:
            elem.draw(drawer=drawer,color=color)

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        for elem in self.page_elements:
            elem.crop(current_dim=current_dim,target_dim=target_dim,cut_left=cut_left)


class MainText(Layout):
    @abstractmethod
    def __init__(self):
        super().__init__()
        self.page_elements: List[MainTextLine] = []
        self.layout_class: LayoutClasses = LayoutClasses.MAINTEXT

    @abstractmethod
    def accept_layout_visitor(self, visitor: LayoutVisitor):
        visitor.visitMainText(self)



class CommentText(Layout):
    pass

class Decorations(Layout):
    pass

class TextRegion(Layout):
    pass