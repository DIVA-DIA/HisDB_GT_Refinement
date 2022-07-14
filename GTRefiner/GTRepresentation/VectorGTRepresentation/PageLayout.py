from __future__ import annotations

from typing import List

from PIL import ImageDraw

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import *
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import PageElement, \
    MainTextLine, CommentTextLine, DecorationElement, TextRegionElement
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Rectangle


# TODO: Test the get_bbox() method.


class Layout(Scalable, Drawable, Croppable, Dictionable):

    @abstractmethod
    def __init__(self, page_elements: List[PageElement] = None):
        if page_elements is None:
            self.page_elements: List[PageElement] = []
        else:
            self.page_elements: List[PageElement] = page_elements
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

    # TODO: Index
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

    def get_bbox(self) -> TextRegionElement:
        bbox: TextRegionElement = TextRegionElement(
            Rectangle([(self.get_min_x(), self.get_min_y()), (self.get_max_x(), self.get_max_y())]))
        return bbox

    def get_min_x(self):
        min_x = float("inf")
        for elem in self.page_elements:
            for coord in elem.polygon.xy:
                if coord[0] < min_x:
                    min_x = int(coord[0])
        return min_x

    def get_min_y(self):
        min_y = float("inf")
        for elem in self.page_elements:
            for coord in elem.polygon.xy:
                if coord[1] < min_y:
                    min_y = int(coord[1])
        return min_y

    def get_max_x(self):
        max_x = 0
        for elem in self.page_elements:
            for coord in elem.polygon.xy:
                if coord[0] > max_x:
                    max_x = int(coord[0])
        return max_x

    def get_max_y(self):
        max_y = 0
        for elem in self.page_elements:
            for coord in elem.polygon.xy:
                if coord[1] > max_y:
                    max_y = int(coord[1])
        return max_y


    def draw(self, drawer: ImageDraw, color: Tuple = None):
        for elem in self.page_elements:
            elem.draw(drawer=drawer, color=color)

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        for elem in self.page_elements:
            elem.crop(current_dim=current_dim, target_dim=target_dim, cut_left=cut_left)

    def build(self) -> Dict:
        dict = {}
        i = 0
        for elem in self.page_elements:
            dict[type(self).__name__ + str(i)] = elem.build()
            i = i+1
        return dict


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

    def __init__(self, layout: Layout = None):
        self.text_regions: List[Layout] = []
        if layout is not None:
            self.add_region(layout)
        self.text_region: TextRegionElement = self.get_bbox()
        super().__init__()
        self.layout_class.append(LayoutClasses.TEXT_REGION)

    def add_region(self, layout: Layout):
        if isinstance(layout, TextRegion):
            raise AttributeError("You're adding a text region in this text region. Use the merge() to do so.")
        self.text_regions.append(layout)

    def merge(self, other: TextRegion):
        pass

    def accept_layout_visitor(self, visitor):
        for layout in self.text_regions:
            layout.accept_layout_visitor(visitor)

    def build(self) -> Dict:
        dict = {}
        for region in self.text_regions:
            region_dict = {}
            region_dict.update(region.build())
            # bbox polygon as text_region id
            dict[str(self.get_bbox().polygon.xy)] = region_dict
        return dict
    
    def get_bbox(self) -> TextRegionElement:
        bbox: TextRegionElement = TextRegionElement(
            Rectangle([(self.get_min_x(), self.get_min_y()), (self.get_max_x(), self.get_max_y())]))
        return bbox

    def get_min_x(self):
        min_x = float("inf")
        for region in self.text_regions:
            for coord in region.get_bbox().polygon.xy:
                if coord[0] < min_x:
                    min_x = int(coord[0])
        return min_x

    def get_min_y(self):
        min_y = float("inf")
        for region in self.text_regions:
            for coord in region.get_bbox().polygon.xy:
                if coord[1] < min_y:
                    min_y = int(coord[1])
        return min_y

    def get_max_x(self):
        max_x = 0
        for region in self.text_regions:
            for coord in region.get_bbox().polygon.xy:
                if coord[0] > max_x:
                    max_x = int(coord[0])
        return max_x

    def get_max_y(self):
        max_y = 0
        for region in self.text_regions:
            for coord in region.get_bbox().polygon.xy:
                if coord[1] > max_y:
                    max_y = int(coord[1])
        return max_y
