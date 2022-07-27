from abc import abstractmethod
from typing import Tuple, List, Dict
import warnings

from PIL import Image, ImageDraw

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Scalable, Drawable, Showable, \
    Croppable, Dictionable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.Layarable import Layarable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import ColorTable, VisibilityTable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Polygon, Line, \
    Quadrilateral, Rectangle


# TODO: accept_json(dict) methode -> json.dump(dict)

class PageElement(Scalable, Drawable, Showable, Croppable, Layarable, Dictionable):
    """ Super class for all page elements, such as decorations & textlines. Every PageElement holds a polygon at its
    core and should be. If further characteristics shall be added, the author suggests to use the decoration pattern.
    :param polygon: Represents the contour of the page element.
    :type polygon: Polygon
    :param color: What color to use when drawn.
    :type color: Tuple
    :param id: To identify the text_line. Helpful for coloring, sorting, etc. Not mandatory, default value is -1.
    :type id: int
    :param is_visible: Whether or not is should be recognized as visible to the :class: `Writer`.
    :type is_visible: bool
    """

    @abstractmethod
    def __init__(self, polygon: Polygon, color: Tuple = (255, 255, 255), is_visible: bool = False, id: int = 0):
        self.polygon: Polygon = polygon
        self.layout_class: LayoutClasses = LayoutClasses.BACKGROUND
        self._id: int = id
        self._color: Tuple = color
        self._is_visible: bool = is_visible

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        self.polygon.resize(current_dim=current_dim, target_dim=target_dim)

    def draw(self, drawer: ImageDraw, color: Tuple = None):
        """ Draw the page element polygon with the instance color if no other coller is given. Fill it, if and only if
        the set_filled parameter is true."""
        if color is None:
            col = self._color
        else:
            col = color
        self.polygon.draw(drawer=drawer, color=col)

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        self.polygon.crop(current_dim=current_dim, target_dim=target_dim, cut_left=cut_left)

    def layer(self, img: Image, layers: List[Layer] = None) -> List[Layer]:
        img_dim: ImageDimension = ImageDimension(img.size[0], img.size[1])
        if not self._is_visible:
            return layers
        layer = Layer(img_dim=img_dim, color=self._color)
        layer.draw(self)
        if layers is None:
            layers = []
        layers.append(layer)
        return layers

    # def layer(self, px_gt: PixelLevelGT):
    # target_layers = self._get_target_layers(px_gt)
    # self._draw_on_target_layers(target_layers=target_layers)
    #
    # def _get_target_layers(self, px_gt: PixelLevelGT) -> List[Layer]:
    #     target_classes: List[LayoutClasses] = LayoutClasses.get_layout_classes_containing(self.layout_class)
    #     target_layers: List[Layer] = []
    #     for target_class in target_classes:
    #         target_layers.append(px_gt.get_layer(target_class))
    #     return target_layers
    #
    # def _draw_on_target_layers(self, target_layers: List[Layer]):
    #     for layer in target_layers:
    #         layer.draw(self)

    def build(self) -> Dict:
        """ Helper function to build the json file. """
        # return {self.layout_class.get_name(): self.polygon.xy} # deprecated
        return {type(self).__name__ + " Coordinates": self.polygon.xy}

    def show(self):
        """ Displays the polygon of the PageElement for debugging purposes d
        """
        # TODO: Maybe delete this method.
        centered_polygon: Polygon = Polygon(
            [(x - self.polygon.get_min_x(), y - self.polygon.get_min_y()) for x, y in self.polygon.xy])
        img_dim: ImageDimension = ImageDimension(width=centered_polygon.get_max_x(),
                                                 height=centered_polygon.get_max_y())
        img = Image.new("RGB", size=img_dim.to_tuple())
        drawer = ImageDraw.Draw(img)
        centered_polygon.draw(drawer=drawer)
        img.show()

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
            colors: List[tuple] = color_table.table[self.layout_class]
            self._color = colors[self._id % len(colors)]

    def get_color(self):
        return self._color

    def get_id(self):
        return self._id

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

    def is_visible(self) -> bool:
        """ Getter-method for the is_visible field.
        :return: Whether or not is should be recognized as visible
        """
        return self._is_visible


class DecorationElement(PageElement):
    """ The :class: `DecorationElement` class has no further characteristic than it's name. It instantiates the abstract super class
    :class: `PageElement`.
    """

    def __init__(self, polygon: Polygon, id: int = 0):
        super().__init__(polygon, id=id)
        self.layout_class = LayoutClasses.DECORATION


class TextLineElements(PageElement):

    @abstractmethod
    def __init__(self, polygon: Polygon, id: int = 0):
        super().__init__(polygon, id=id)


class BaseLine(TextLineElements):

    def __init__(self, base_line: Line, id: int = 0):
        super().__init__(base_line, id=id)
        self.layout_class = LayoutClasses.BASELINE

    def set_visible(self, is_visible: bool = None, vis_table: VisibilityTable = None):
        if is_visible is True:
            warnings.warn(f"It's not recommended to set this object {type(self).__name__} visible.")
        super().set_visible(is_visible=is_visible, vis_table=vis_table)


class TopLine(TextLineElements):

    def __init__(self, base_line: BaseLine, x_height: int, id: int = 0):
        line = Line([tuple((x, y - x_height)) for x, y in base_line.polygon.xy])
        super().__init__(line, id=id)
        self.layout_class = LayoutClasses.TOPLINE

    def set_visible(self, is_visible: bool = None, vis_table: VisibilityTable = None):
        if is_visible is True:
            warnings.warn(f"It's not recommended to set this object {type(self).__name__} visible.")
        super().set_visible(is_visible=is_visible, vis_table=vis_table)


class XRegion(TextLineElements):

    def __init__(self, base_line: BaseLine, top_line: TopLine, id: int = 0):
        # sorted_baseline = [base_line.polygon.xy[1], base_line.polygon.xy[0]]
        # top_line =
        concatenated = [top_line.polygon.xy[0], top_line.polygon.xy[1], base_line.polygon.xy[1],
                        base_line.polygon.xy[0]]
        quadrilateral = Quadrilateral(concatenated)
        super().__init__(quadrilateral, id=id)
        self.layout_class = LayoutClasses.XREGION

    def layer(self, img: Image, layers: List[Layer] = None) -> List[Layer]:
        if not self.polygon.is_sorted():
            raise AttributeError("Quadrilateral must be sorted. Something went wrong.")
        return super().layer(img=img, layers=layers)


class AscenderRegion(TextLineElements):

    def __init__(self, polygon: Polygon, top_line: TopLine, id: int = 0):
        min_x = polygon.get_min_x()
        min_y = polygon.get_min_y()
        max_x = polygon.get_max_x()
        self.region = Quadrilateral([(min_x, min_y),  # left top corner
                                     (max_x, min_y),  # right top corner
                                     top_line.polygon.get_max_x_coord(),  # right bottom corner
                                     top_line.polygon.get_min_x_coord()  # left bottom corner
                                     ])
        super().__init__(self.region, id=id)
        self.layout_class = LayoutClasses.ASCENDER
        # TODO: check if get_max_x_coord is called.


class DescenderRegion(TextLineElements):

    def __init__(self, polygon: Polygon, base_line: BaseLine, id: int = 0):
        min_x = polygon.get_min_x()
        max_x = polygon.get_max_x()
        max_y = polygon.get_max_y()
        region = Quadrilateral([base_line.polygon.get_min_x_coord(),  # left top corner
                                base_line.polygon.get_max_x_coord(),  # right top corner
                                (max_x, max_y),  # right bottom corner
                                (min_x, max_y)  # left bottom corner
                                ])
        super().__init__(region, id=id)
        self.layout_class = LayoutClasses.DESCENDER


class TextRegionElement(TextLineElements):

    def __init__(self, bounding_box: Rectangle, id: int = 0):
        super().__init__(bounding_box, id=id)
        self.layout_class = LayoutClasses.TEXT_REGION

    def set_is_filled(self, is_filled: bool):
        """Text Regions should not drawn as filled boxes."""
        pass


class TextLine(PageElement):
    """ Represents all PageElements with text line characteristics. Examples are comment lines and main-text lines.
    :param polygon: represents the contour of the text line.
    :type polygon: Polygon
    :param base_line: Every :class: `TextLine` class comes with a default base_line provided by the original xml_gt.
    :type base_line: Line
    """

    @abstractmethod
    def __init__(self, polygon: Polygon, base_line: BaseLine, color: Tuple = (255, 255, 255),
                 is_visible: bool = True, id: int = 0):
        super().__init__(polygon, color=color, is_visible=is_visible, id=id)
        self.base_line: BaseLine = base_line

    def draw(self, drawer: ImageDraw, color: Tuple = None):
        super().draw(drawer=drawer, color=color)
        # self.base_line.draw(drawer, color=color)

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        super().resize(current_dim, target_dim)
        self.base_line.resize(current_dim=current_dim, target_dim=target_dim)

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        super().crop(current_dim, target_dim, cut_left)
        self.base_line.crop(current_dim=current_dim, target_dim=target_dim, cut_left=cut_left)

    def layer(self, img: Image, layers: List[Layer] = None) -> List[Layer]:
        layers: List[Layer] = super().layer(img=img, layers=layers)
        return self.base_line.layer(img=img, layers=layers)

    def build(self) -> Dict:
        data: Dict = super().build()
        data.update(self.base_line.build())  # add base_line
        return {self.layout_class.get_name(): data}

    def set_color(self, color: Tuple = None, color_table: ColorTable = None):
        super().set_color(color, color_table)
        self.base_line.set_color(color=color, color_table=color_table)

    def set_visible(self, is_visible: bool = None, vis_table: VisibilityTable = None):
        super().set_visible(is_visible=is_visible, vis_table=vis_table)


class MainTextLine(TextLine):
    """ The :class: `MainTextLine` class has no further characteristic than it's name. It instantiates the abstract super class
    :class: `PageElement`.
    """

    def __init__(self, polygon: Polygon, base_line: BaseLine, color: Tuple = (255, 255, 255), is_filled: bool = False,
                 is_visible: bool = True, id: int = 0):
        super().__init__(polygon, base_line, color=color, is_visible=is_visible, id=id)
        self.layout_class = LayoutClasses.MAINTEXT


class CommentTextLine(TextLine):
    """ The :class: `CommentTextLine` class has no further characteristic than it's name. It instantiates the abstract super class
    :class: `PageElement`.
    """

    def __init__(self, polygon: Polygon, base_line: BaseLine, color: Tuple = (255, 255, 255), is_filled: bool = False,
                 is_visible: bool = True, id: int = 0):
        super().__init__(polygon, base_line, color=color, is_visible=is_visible, id=id)
        self.layout_class = LayoutClasses.COMMENT


class TextLineDecoration(TextLine):
    """ Decorator class used to add further functionalities to :class: `TextLine` page elements.
    """

    @abstractmethod
    def __init__(self, text_line: TextLine):
        super().__init__(text_line.polygon, text_line.base_line, color=text_line._color,
                         is_visible=text_line._is_visible, id=text_line.get_id())
        self.text_line: TextLine = text_line
        # self.layout_class = text_line.layout_class

    @abstractmethod
    def draw(self, drawer: ImageDraw, color: Tuple = None):
        super().draw(drawer=drawer, color=color)

    @abstractmethod
    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        super().resize(current_dim, target_dim)

    @abstractmethod
    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        super().crop(current_dim, target_dim, cut_left)

    @abstractmethod
    def show(self):
        super().show()

    @abstractmethod
    def set_color(self, color: Tuple = None, color_table: ColorTable = None):
        super().set_color(color, color_table)

    @abstractmethod
    def set_visible(self, is_visible: bool = None, vis_table: VisibilityTable = None):
        super().set_visible(is_visible=is_visible, vis_table=vis_table)


class AscenderDescenderRegion(TextLineDecoration):
    """ Decorator of Textline which adds an x-region, ascender- and descender-region.
    :param text_line: Textline to be decorated.
    :param top_line: Represents the top line of x_region.
    :type top_line: Line
    :param x_region: Denotes the region for little x.
    :type x_region: Quadrilateral
    :param ascender_region: Denotes the region of ascenders.
    :type ascender_region: Quadrilateral
    :param descender_region: Denotes the region of descenders.
    :type descender_region: Quadrilateral
    The rest of the parameters are used to give custom colors to each of the :class:`Polygon` vectorobjects for
    debugging purposes the different fields have.
    """

    def __init__(self, text_line: TextLine, x_height: int):
        super().__init__(text_line)
        self.x_height: int = x_height
        assert x_height > 0
        # max_value_possible = self.base_line.polygon.get_min_y() - self.text_line.polygon.get_min_y()
        # if x_height > max_value_possible:
        #     raise AttributeError("The x_height seems is too big. The topline would be outside the boundary box. /n "
        #                          "Choose a smaller x_height. The current x_height is: " + str(
        #         x_height) + "max value allowed: " + str(max_value_possible))
        # vector_objects
        self.top_line: TopLine = TopLine(base_line=self.base_line, x_height=x_height, id=text_line.get_id())
        self.x_region: XRegion = XRegion(base_line=self.base_line, top_line=self.top_line, id=text_line.get_id())
        self.ascender_region: AscenderRegion = AscenderRegion(polygon=text_line.polygon, top_line=self.top_line, id=text_line.get_id())
        self.descender_region: DescenderRegion = DescenderRegion(polygon=text_line.polygon, base_line=self.base_line, id=text_line.get_id())
        self.layout_class = text_line.layout_class
        # # add layout class of decorators to the list
        # self.layout_class.extend(self.top_line.layout_class)
        # self.layout_class.extend(self.x_region.layout_class)
        # self.layout_class.extend(self.ascender_region.layout_class)
        # self.layout_class.extend(self.descender_region.layout_class)

    def draw(self, drawer: ImageDraw, color: Tuple = None):
        # self.top_line.draw(drawer, color=color)
        # self.x_region.draw(drawer, color=color)
        # self.ascender_region.draw(drawer, color=color)
        # self.descender_region.draw(drawer, color=color)
        super().draw(drawer=drawer, color=color)

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        super().resize(current_dim, target_dim)
        self.top_line.resize(current_dim, target_dim)
        self.x_region.resize(current_dim, target_dim)
        self.ascender_region.resize(current_dim, target_dim)
        self.descender_region.resize(current_dim, target_dim)

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        super().crop(current_dim, target_dim, cut_left)
        self.top_line.crop(current_dim, target_dim, cut_left)
        self.x_region.crop(current_dim, target_dim, cut_left)
        self.ascender_region.crop(current_dim, target_dim, cut_left)
        self.descender_region.crop(current_dim, target_dim, cut_left)

    def layer(self, img: Image, layers: List[Layer] = None):
        layers: List[Layer] = super().layer(img=img, layers=layers)
        layers: List[Layer] = self.top_line.layer(img=img, layers=layers)
        layers: List[Layer] = self.x_region.layer(img=img, layers=layers)
        layers: List[Layer] = self.ascender_region.layer(img=img, layers=layers)
        return self.descender_region.layer(img=img, layers=layers)

    def build(self) -> Dict:
        data: Dict = super().build()
        data.update(self.top_line.build())  # add base_line
        data.update(self.ascender_region.build())
        data.update(self.descender_region.build())
        data.update(self.x_region.build())
        return data

    def show(self):
        super().show()
        # raise Warning("The show method in asc_desc_region is not implemented.")
        warnings.warn("The show method in asc_desc_region is not imlemented.", DeprecationWarning)

    def set_color(self, color: Tuple = None, color_table: ColorTable = None):
        super().set_color(color, color_table)
        self.top_line.set_color(color=color, color_table=color_table)
        self.x_region.set_color(color=color, color_table=color_table)
        self.ascender_region.set_color(color=color, color_table=color_table)
        self.descender_region.set_color(color=color, color_table=color_table)

    def set_visible(self, is_visible: bool = None, vis_table: VisibilityTable = None):
        super().set_visible(is_visible=is_visible, vis_table=vis_table)
        self.x_region.set_visible(is_visible=is_visible, vis_table=vis_table)
        self.ascender_region.set_visible(is_visible=is_visible, vis_table=vis_table)
        self.descender_region.set_visible(is_visible=is_visible, vis_table=vis_table)


class HeadAndTailRegion(TextLine):
    pass


class Histogram(TextLine):
    pass
