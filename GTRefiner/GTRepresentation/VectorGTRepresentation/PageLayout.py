from __future__ import annotations

from typing import List

from PIL import ImageDraw, Image

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import *
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.Layarable import Layarable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import ColorTable, VisibilityTable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import PageElement, \
    TextRegionElement
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Rectangle


# TODO: Test the get_bbox() method.


class Layout(Scalable, Drawable, Croppable, Dictionable, Layarable):
    """
    :param page_elements: List of all page elements of a layout (e.g. comment text lines or decorations).
    :type page_elements: List[PageElement]
    :param layout_class: The class of the layout (e.g. COMMENT or DECORATION)
    :type layout_class: LayoutClasses
    """

    def __init__(self, page_elements: List[PageElement] = None, layout_class: LayoutClasses = None):
        """ Constructor Method """
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

    def set_color(self, color: Tuple = None, color_table: ColorTable = None):
        """ Setter-method for the color.
        :param color: What color to use when drawn.
        :type color: Tuple
        """
        if (color is None) and (color_table is None):
            raise AttributeError("Either give color or color_table, not None")
        if (color is not None) and (color_table is not None):
            raise AttributeError("Either give color or color_table, not both")
        if color is not None:
            self._color = color
        if color_table is not None:
            if self.layout_class in color_table.table.keys():
                self._color = color_table[self.layout_class]

    def set_visible(self, is_visible: bool = None, vis_table: VisibilityTable = None):
        """ Setter-method for the is_visible field.
        :param is_visible: Whether or not is should be recognized as visible
        :type is_visible: bool
        """
        if (is_visible is None) and (vis_table is None):
            raise AttributeError("Either give color or color_table, not None")
        if (is_visible is not None) and (vis_table is not None):
            raise AttributeError("Either give color or color_table, not both")
        if is_visible is not None:
            self._is_visible = is_visible
        if vis_table is not None:
            self._is_visible = vis_table.table[self.layout_class]

    def add_elem(self, elem: PageElement):
        """ Append an element to this layout. Can also be done with the built-in function append, however this method is
        is safer.
        :param elem:
        :type elem:
        :return:
        :rtype:
        """
        if not elem.layout_class == self.layout_class:
            raise AttributeError(
                f"Cannot add element of a different layout_class. elem.layout_class = {elem.layout_class},"
                f"self.layout_class = {self.layout_class} ")
        self.page_elements.append(elem)

    def layer(self, img: Image):
        """ Returns a image of all layers for every PageElement according to the order chosen with
        the implementation. (We suggest, you change it to a dict of LayoutClasses and Layers for a safer implementation.)
        :param img: base img to be drawn upon.
        :type img: Image
        TODO: Make safer with dict.
        """
        for elem in self.page_elements:
            if elem.is_visible():
                layers: List[Layer] = elem.layer(img=img)
                img = Layer.merge_and_draw(layers=layers, img=img)
        return img

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        """Resizes all page elements :class: `List[PageElement]` of the current :class: `LayoutClass` to a given target
        dimension. As this class doesn't possess a image dimension parameter, both the current dimension (of the page)
        and the target dimension (the size to be scaled to) must be given.
        :param current_dim: Current dimension
        :type current_dim: ImageDimension
        :param target_dim: Target dimension
        :type target_dim: ImageDimension
        """
        for elem in self.page_elements:
            elem.resize(current_dim=current_dim, target_dim=target_dim)

    def get_region_bbox(self) -> TextRegionElement:
        """ Dynamically returns a TextRegion element."""
        bbox: TextRegionElement = TextRegionElement(
            Rectangle([(self._get_min_x(), self._get_min_y()), (self._get_max_x(), self._get_max_y())]))
        return bbox

    def _get_min_x(self) -> int:
        """ Return the min x-coordinate of all page elements in this layout.
        :return: min x-coordinate of all page elements in this layout
        :rtype: int
        """
        min_x = float("inf")
        for elem in self.page_elements:
            for coord in elem.polygon.xy:
                if coord[0] < min_x:
                    min_x = int(coord[0])
        return min_x

    def _get_min_y(self):
        """ Return the min y-coordinate of all page elements in this layout.
        :return: min y-coordinate of all page elements in this layout
        :rtype: int
        """
        min_y = float("inf")
        for elem in self.page_elements:
            for coord in elem.polygon.xy:
                if coord[1] < min_y:
                    min_y = int(coord[1])
        return min_y

    def _get_max_x(self):
        """ Return the max x-coordinate of all page elements in this layout.
        :return: max x-coordinate of all page elements in this layout
        :rtype: int
        """
        max_x = 0
        for elem in self.page_elements:
            for coord in elem.polygon.xy:
                if coord[0] > max_x:
                    max_x = int(coord[0])
        return max_x

    def _get_max_y(self):
        """ Return the max y-coordinate of all page elements in this layout.
        :return: max y-coordinate of all page elements in this layout
        :rtype: int
        """
        max_y = 0
        for elem in self.page_elements:
            for coord in elem.polygon.xy:
                if coord[1] > max_y:
                    max_y = int(coord[1])
        return max_y

    def draw(self, drawer: ImageDraw, color: Tuple = None, outline=None):
        """ If layout is visible, draw all page elements of this layout on the given image in a certain color and
        outline.
        :param drawer: image to be drawn upon.
        :type drawer: ImageDraw.ImageDraw
        :param color: fill of the object. Can be of any mode that pillow understands (e.g. RGBA, 1, L, RGB).
        :type color: tuple
        :param outline: outline of the object. Should only be used for illustration purposes!
        Can be of any mode that pillow understands (e.g. RGBA, 1, L, RGB).
        :type outline: tuple"""
        if self._is_visible:
            self.get_region_bbox().draw(drawer=drawer, color=color, outline=outline)
        for elem in self.page_elements:
            elem.draw(drawer=drawer, color=color, outline=None)

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        """ Crop all page elements of this layout to a target dimension. Due to the nature of the ground truth document
        :param cut_left: must be provided.
        :param current_dim: Current dimension
        :type current_dim: ImageDimension
        :param target_dim: Target dimension
        :type target_dim: ImageDimension
        :param cut_left: Whether or not the page is cut_left or not.
        :type cut_left: bool
        """
        for elem in self.page_elements:
            elem.crop(current_dim=current_dim, target_dim=target_dim, cut_left=cut_left)

    def build(self) -> Dict:
        dict = {}
        i = 0
        for elem in self.page_elements:
            dict[type(self).__name__ + str(i)] = elem.build()
            i = i + 1
        return dict

    def merge(self, other: Layout):
        """ Merge this layout with another one. Doesn't do any layout_class checks. Client must be sure that they are
        both of the same layout class."""
        self.page_elements.extend(other.page_elements)

    def __getitem__(self, item):
        return self.page_elements[item]

    def __setitem__(self, key, value):
        self.page_elements[key] = value

    def __lt__(self, other: Layout):
        return self._get_min_x() < other._get_min_x()


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
        """ Add a layout to the region. Doesn't do any layout_class checks. Client must be sure that they are
        both of the same layout class.
        :param layout: Layout to be added to the region.
        :type layout: Layout
        """
        if self.layout_class is None and layout is not None:
            self.layout_class = layout.layout_class
        if not layout.layout_class == self.layout_class:
            raise AttributeError(f"The layout to be added doesn't match the region's layout_class."
                                 f"self.layout_class = {self.layout_class}, layout.layout_class = {layout.layout_class}")
        self.text_regions.append(layout)

    def layer(self, img: Image):
        """ Returns a image of all layers for every layout on the corresponding layer according to the order chosen with
        the implementation.
        :param img: base img to be drawn upon.
        :type img: Image
        """
        for layout in self.text_regions:
            # if LayoutClasses.COMMENT == layout.layout_class:
            #     print("here's your comment")
            img = layout.layer(img)
        return img

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

    def sort_layout_elements(self, reverse: bool = False):
        """ Sorts the page_elements of a text_region by the min y value of the page elements. """
        layout: Layout
        for i, layout in enumerate(self.text_regions):
            list.sort(layout.page_elements, key=PageElement, reverse=reverse)
        # assertion
        assert self._is_sorted(reverse)

    def _is_sorted(self, reverse=False) -> bool:
        """Helper method of sort(). Check if all page elements are sorted accordingly."""
        for layout in self.text_regions:
            for i, elem in enumerate(layout.page_elements[1:]):
                prev = layout.page_elements[i].get_min_y()
                curr = layout.page_elements[i + 1].get_min_y()
                print(f"Layout: {layout.layout_class}, counter: {i} "
                      f"previous y: {prev}, current y: {curr}")
                if reverse == False:
                    is_sorted: bool = prev <= curr
                else:
                    is_sorted: bool = prev >= curr
        return is_sorted

    def __getitem__(self, item):
        return self.text_regions[item]

    def __setitem__(self, key, value):
        self.text_regions[key] = value
