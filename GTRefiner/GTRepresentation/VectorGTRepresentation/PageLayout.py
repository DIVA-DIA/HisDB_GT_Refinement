from __future__ import annotations

from typing import List

from PIL import ImageDraw, Image

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import *
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.Layarable import Layarable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import PageElement, \
    MainTextLine, CommentTextLine, DecorationElement, TextRegionElement, AscenderDescenderRegion
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Rectangle


# TODO: Test the get_bbox() method.


class Layout(Scalable, Drawable, Croppable, Dictionable, Layarable):

    def __init__(self, page_elements: List[PageElement] = None, layout_class: LayoutClasses = None):
        if page_elements is None and layout_class is None:
            self.page_elements: List[PageElement] = []
            self.layout_class: LayoutClasses = None
        elif page_elements is None and layout_class is not None:
            self.page_elements: List[PageElement] = []
            self.layout_class: LayoutClasses = layout_class
        elif page_elements is not None and layout_class is not None:
            self.page_elements: List[PageElement] = page_elements
            self.layout_class: LayoutClasses = layout_class
        elif page_elements is not None and layout_class is None:
            raise AttributeError("Must provide layout_class if page_elements are given.")
        self._color: Tuple = (255, 255, 255)  # not yet used, could be useful for future implementation of Colorer
        self._is_visible: bool = True  # not yet used, could be useful for future implementation of Colorer or Combiner
                                        # (Layerer)

    @abstractmethod
    def accept_layout_visitor(self, visitor):
        pass

    def set_color(self, color: Tuple):
        self._color = color

    def set_visible(self, is_visible: bool):
        self._is_visible = is_visible

    def add_elem(self, elem: PageElement):
        self.page_elements.append(elem)
        if not elem.layout_class == self.layout_class:
            raise AttributeError(
                f"Cannot add element of a different layout_class. elem.layout_class = {elem.layout_class},"
                f"self.layout_class = {self.layout_class} ")

    def layer(self, img: Image):
        for elem in self.page_elements:
            if elem.is_visible():
                layers: List[Layer] = elem.layer(img=img)
                img = Layer.merge_and_draw(layers=layers, img=img)
        return img

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        for elem in self.page_elements:
            elem.resize(current_dim=current_dim, target_dim=target_dim)

    def get_region_bbox(self) -> TextRegionElement:
        bbox: TextRegionElement = TextRegionElement(
            Rectangle([(self._get_min_x(), self._get_min_y()), (self._get_max_x(), self._get_max_y())]))
        return bbox

    def _get_min_x(self):
        min_x = float("inf")
        for elem in self.page_elements:
            for coord in elem.polygon.xy:
                if coord[0] < min_x:
                    min_x = int(coord[0])
        return min_x

    def _get_min_y(self):
        min_y = float("inf")
        for elem in self.page_elements:
            for coord in elem.polygon.xy:
                if coord[1] < min_y:
                    min_y = int(coord[1])
        return min_y

    def _get_max_x(self):
        max_x = 0
        for elem in self.page_elements:
            for coord in elem.polygon.xy:
                if coord[0] > max_x:
                    max_x = int(coord[0])
        return max_x

    def _get_max_y(self):
        max_y = 0
        for elem in self.page_elements:
            for coord in elem.polygon.xy:
                if coord[1] > max_y:
                    max_y = int(coord[1])
        return max_y

    def draw(self, drawer: ImageDraw, color: Tuple = None, outline=None):
        for elem in self.page_elements:
            elem.draw(drawer=drawer, color=color, outline=None)

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        for elem in self.page_elements:
            elem.crop(current_dim=current_dim, target_dim=target_dim, cut_left=cut_left)

    def build(self) -> Dict:
        dict = {}
        i = 0
        for elem in self.page_elements:
            dict[type(self).__name__ + str(i)] = elem.build()
            i = i + 1
        return dict

    def __getitem__(self, item):
        return self.page_elements[item]

    def __setitem__(self, key, value):
        self.page_elements[key] = value

class TextRegion(Layout):

    def __init__(self, layout: Layout = None, text_regions: List[Layout] = None):
        if text_regions is None:
            self.text_regions: List[Layout] = []
        self.text_region: TextRegionElement
        super().__init__()
        # self.layout_class.append(LayoutClasses.TEXT_REGION)
        if text_regions is not None:
            self.text_regions: List[Layout] = text_regions
            self.text_region: TextRegionElement = self.get_region_bbox()
            self.layout_class = self.text_regions[0].layout_class
        if layout is not None:
            self.layout_class = layout.layout_class
            self.add_region(layout)
            self.text_region = self.get_region_bbox()

    def add_region(self, layout: Layout):
        if not layout.layout_class == self.layout_class:
            raise AttributeError(f"The layout to be added doesn't match the region's layout_class."
                                 f"self.layout_class = {self.layout_class}, layout.layout_class = {layout.layout_class}")
        if self.layout_class is None:
            self.layout_class = layout.layout_class
        self.text_regions.append(layout)

    def layer(self, img: Image):
        for layout in self.text_regions:
            # if LayoutClasses.COMMENT == layout.layout_class:
            #     print("here's your comment")
            img = layout.layer(img)
        return img

    def accept_layout_visitor(self, visitor):
        for layout in self.text_regions:
            layout.accept_layout_visitor(visitor)

    def build(self) -> Dict:
        dict = {}
        for region in self.text_regions:
            region_dict = {}
            region_dict.update(region.build())
            # bbox polygon as text_region id
            dict[str(self.get_region_bbox().polygon.xy)] = region_dict
        return dict

    def get_region_bbox(self) -> TextRegionElement:
        bbox: TextRegionElement = TextRegionElement(
            Rectangle([(self._get_min_x(), self._get_min_y()), (self._get_max_x(), self._get_max_y())]))
        return bbox

    def _get_min_x(self):
        min_x = float("inf")
        for region in self.text_regions:
            for coord in region.get_region_bbox().polygon.xy:
                if coord[0] < min_x:
                    min_x = int(coord[0])
        return min_x

    def _get_min_y(self):
        min_y = float("inf")
        for region in self.text_regions:
            for coord in region.get_region_bbox().polygon.xy:
                if coord[1] < min_y:
                    min_y = int(coord[1])
        return min_y

    def _get_max_x(self):
        max_x = 0
        for region in self.text_regions:
            for coord in region.get_region_bbox().polygon.xy:
                if coord[0] > max_x:
                    max_x = int(coord[0])
        return max_x

    def _get_max_y(self):
        max_y = 0
        for region in self.text_regions:
            for coord in region.get_region_bbox().polygon.xy:
                if coord[1] > max_y:
                    max_y = int(coord[1])
        return max_y
