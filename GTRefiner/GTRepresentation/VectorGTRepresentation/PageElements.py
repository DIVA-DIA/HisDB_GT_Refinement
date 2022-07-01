from abc import abstractmethod
from typing import Tuple, List
import warnings

from PIL import Image, ImageDraw

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Scalable, Drawable, Showable, \
    Croppable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Polygon, Line, \
    Quadrilateral


class PageElement(Scalable, Drawable, Showable, Croppable):
    """ Super class for all page elements, such as decorations & textlines. Every PageElement holds a polygon at its
    core and should be. If further characteristics shall be added, the author suggests to use the decoration pattern.
    :param polygon: Represents the contour of the page element.
    :type polygon: Polygon
    :param color: What color to use when drawn.
    :type color: Tuple
    :param is_filled: Whether or not the polygon should be filled. Deprecated for decorated page elements.
    :type is_filled: bool
    :param is_visible: Wether or not is should be recognized as visible to the :class: `Writer`.
    :type is_visible: bool
    """

    @abstractmethod
    def __init__(self, polygon: Polygon, color: Tuple = (255, 255, 255), is_filled: bool = False,
                 is_visible: bool = True):
        self.polygon: Polygon = polygon
        self.layout_class: List[LayoutClasses] = []
        self.color: Tuple = color
        self.is_filled: bool = is_filled
        self.is_visible: bool = is_visible

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        self.polygon.resize(current_dim=current_dim, target_dim=target_dim)

    def draw(self, drawer: ImageDraw, color: Tuple = None):
        """ Draw the page element polygon with the instance color if no other coller is given. Fill it, if and only if
        the set_filled parameter is true."""
        if color is None:
            col = self.color
        else:
            col = color
        fill = None
        if self.is_filled is True:
            fill = col
        self.polygon.draw(drawer=drawer, outline=col, fill=fill)

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        self.polygon.crop(current_dim=current_dim, target_dim=target_dim, cut_left=cut_left)

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
        centered_polygon.draw(drawer=drawer, outline=(255, 43, 23))
        img.show()

    def set_color(self, color: Tuple):
        """ Setter-method for the color.
        :param color: What color to use when drawn.
        :type color: Tuple
        """
        self.color = color

    def set_is_filled(self, is_filled: bool):
        """ Setter-method for the is_filled field.
        :param is_filled: Whether or not the polygon should be filled. Deprecated for decorated page elements.
        :type is_filled: bool
        """
        self.is_filled = is_filled

    def set_is_visible(self, is_visible: bool):
        """ Setter-method for the is_visible field.
        :param is_visible: Wether or not is should be recognized as visible to the :class: `Writer`.
        :type is_visible: bool
        """
        self.is_visible = is_visible

    def get_layout_class(self) -> List[LayoutClasses]:
        return self.layout_class


class DecorationElement(PageElement):
    """ The :class: `DecorationElement` class has no further characteristic than it's name. It instantiates the abstract super class
    :class: `PageElement`.
    """

    def __init__(self, polygon: Polygon):
        super().__init__(polygon)
        self.layout_class.append(LayoutClasses.DECORATION)


class TextLineElements(PageElement):

    @abstractmethod
    def __init__(self, polygon: Polygon):
        super().__init__(polygon)


class BaseLine(TextLineElements):

    def __init__(self, base_line: Line):
        super().__init__(base_line)
        self.layout_class.append(LayoutClasses.BASELINE)


class TopLine(TextLineElements):

    def __init__(self, base_line: BaseLine, x_height: int):
        line = Line([tuple((x, y - x_height)) for x, y in base_line.polygon.xy])
        super().__init__(line)
        self.layout_class.append(LayoutClasses.TOPLINE)


class XRegion(TextLineElements):

    def __init__(self, base_line: BaseLine, top_line: TopLine):
        sorted_baseline = [base_line.polygon.xy[1], base_line.polygon.xy[0]]
        top_line = top_line.polygon.xy
        concatenated = top_line + sorted_baseline
        quadrilateral = Quadrilateral(concatenated)
        super().__init__(quadrilateral)
        self.layout_class.append(LayoutClasses.XREGION)


class AscenderRegion(TextLineElements):

    def __init__(self, polygon: Polygon, top_line: TopLine):
        min_x = polygon.get_min_x()
        min_y = polygon.get_min_y()
        max_x = polygon.get_max_x()
        self.region = Quadrilateral([(min_x, min_y),  # left top corner
                                     (max_x, min_y),  # right top corner
                                     top_line.polygon.get_max_x_coord(),  # right bottom corner
                                     top_line.polygon.get_min_x_coord()  # left bottom corner
                                     ])
        super().__init__(self.region)
        self.layout_class.append(LayoutClasses.ASCENDER)
        # TODO: check if get_max_x_coord is called.


class DescenderRegion(TextLineElements):

    def __init__(self, polygon: Polygon, base_line: BaseLine):
        min_x = polygon.get_min_x()
        max_x = polygon.get_max_x()
        max_y = polygon.get_max_y()
        region = Quadrilateral([base_line.polygon.get_min_x_coord(),  # left top corner
                                base_line.polygon.get_max_x_coord(),  # right top corner
                                (max_x, max_y),  # right bottom corner
                                (min_x, max_y)  # left bottom corner
                                ])
        super().__init__(region)
        self.layout_class.append(LayoutClasses.DESCENDER)


class TextLine(PageElement):
    """ Represents all PageElements with text line characteristics. Examples are comment lines and main-text lines.
    :param polygon: represents the contour of the text line.
    :type polygon: Polygon
    :param base_line: Every :class: `TextLine` class comes with a default base_line provided by the original xml_gt.
    :type base_line: Line
    """

    @abstractmethod
    def __init__(self, polygon: Polygon, base_line: BaseLine, color: Tuple = (255, 255, 255), is_filled: bool = False,
                 is_visible: bool = True):
        super().__init__(polygon, color=color, is_filled=is_filled, is_visible=is_visible)
        self.base_line: BaseLine = base_line

    def draw(self, drawer: ImageDraw, color: Tuple = None):
        super().draw(drawer, color=color)
        self.base_line.draw(drawer, color=color)

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        super().resize(current_dim, target_dim)
        self.base_line.resize(current_dim=current_dim, target_dim=target_dim)

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        super().crop(current_dim, target_dim, cut_left)
        self.base_line.crop(current_dim=current_dim, target_dim=target_dim, cut_left=cut_left)

    def set_color(self, color: Tuple):
        super().set_color(color)
        self.base_line.set_color(color=color)

    def set_is_filled(self, is_filled: bool):
        super().set_is_filled(is_filled)
        self.base_line.set_is_filled(is_filled=is_filled)

    def set_is_visible(self, is_visible: bool):
        super().set_is_visible(is_visible)
        self.base_line.set_is_visible(is_visible=is_visible)


class MainTextLine(TextLine):
    """ The :class: `MainTextLine` class has no further characteristic than it's name. It instantiates the abstract super class
    :class: `PageElement`.
    """

    def __init__(self, polygon: Polygon, base_line: BaseLine, color: Tuple = (255, 255, 255), is_filled: bool = False,
                 is_visible: bool = True):
        super().__init__(polygon, base_line, color=color, is_filled=is_filled, is_visible=is_visible)
        self.layout_class.append(LayoutClasses.MAINTEXT)


class CommentTextLine(TextLine):
    """ The :class: `CommentTextLine` class has no further characteristic than it's name. It instantiates the abstract super class
    :class: `PageElement`.
    """

    def __init__(self, polygon: Polygon, base_line: BaseLine, color: Tuple = (255, 255, 255), is_filled: bool = False,
                 is_visible: bool = True):
        super().__init__(polygon, base_line, color=color, is_filled=is_filled, is_visible=is_visible)
        self.layout_class.append(LayoutClasses.COMMENT)


class TextLineDecoration(TextLine):
    """ Decorator class used to add further functionalities to :class: `TextLine` page elements.
    """

    @abstractmethod
    def __init__(self, text_line: TextLine):
        super().__init__(text_line.polygon, text_line.base_line, color=text_line.color, is_filled=text_line.is_filled,
                         is_visible=text_line.is_visible)
        self.text_line: TextLine = text_line
        self.layout_class.extend(text_line.layout_class)

    @abstractmethod
    def draw(self, drawer: ImageDraw, color: Tuple = None):
        super().draw(drawer, color)

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
    def set_color(self, color: Tuple):
        super().set_color(color)

    @abstractmethod
    def set_is_filled(self, is_filled: bool):
        super().set_is_filled(is_filled)

    @abstractmethod
    def set_is_visible(self, is_visible: bool):
        super().set_is_visible(is_visible)


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
        if self.base_line.polygon.get_min_y() - x_height < self.text_line.polygon.get_min_y():
            raise AttributeError("The x_height seems is too big. The topline would be outside the boundary box. /n "
                                 "Choose a smaller x_height. The current x_height is: " + str(x_height))
        # vector_objects
        self.top_line: TopLine = TopLine(base_line=self.base_line, x_height=x_height)
        self.x_region: XRegion = XRegion(base_line=self.base_line, top_line=self.top_line)
        self.ascender_region: AscenderRegion = AscenderRegion(polygon=text_line.polygon, top_line=self.top_line)
        self.descender_region: DescenderRegion = DescenderRegion(polygon=text_line.polygon, base_line=self.base_line)
        # add layout class of decorators to the list
        self.layout_class.extend(self.top_line.layout_class)
        self.layout_class.extend(self.x_region.layout_class)
        self.layout_class.extend(self.ascender_region.layout_class)
        self.layout_class.extend(self.descender_region.layout_class)

    def draw(self, drawer: ImageDraw, color: Tuple = None):
        self.top_line.draw(drawer, color=color)
        self.x_region.draw(drawer, color=color)
        self.ascender_region.draw(drawer, color=color)
        self.descender_region.draw(drawer, color=color)
        super().draw(drawer, color)

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

    def show(self):
        super().show()
        # raise Warning("The show method in asc_desc_region is not implemented.")
        warnings.warn("The show method in asc_desc_region is not imlemented.", DeprecationWarning)

    def set_color(self, color: Tuple):
        super().set_color(color)
        self.top_line.set_color(color=color)
        self.x_region.set_color(color=color)
        self.ascender_region.set_color(color=color)
        self.descender_region.set_color(color=color)

    def set_is_filled(self, is_filled: bool):
        super().set_is_filled(is_filled)
        self.top_line.set_is_filled(is_filled=is_filled)
        self.x_region.set_is_filled(is_filled=is_filled)
        self.ascender_region.set_is_filled(is_filled=is_filled)
        self.descender_region.set_is_filled(is_filled=is_filled)

    def set_is_visible(self, is_visible: bool):
        super().set_is_visible(is_visible)
        self.top_line.set_is_visible(is_visible=is_visible)
        self.x_region.set_is_visible(is_visible=is_visible)
        self.ascender_region.set_is_visible(is_visible=is_visible)
        self.descender_region.set_is_visible(is_visible=is_visible)


class HeadAndTailRegion(TextLine):
    pass


class Histogram(TextLine):
    pass
