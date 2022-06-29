from abc import abstractmethod
from typing import Tuple
import warnings

from PIL import Image, ImageDraw

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GTInterfaces import Scalable, Drawable, Showable, Croppable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
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
        self.color: Tuple = color
        self.is_filled: bool = is_filled
        self.is_visible: bool = is_visible

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        self.polygon.resize(current_dim=current_dim, target_dim=target_dim)

    def draw(self, drawer: ImageDraw, color: Tuple = None, is_filled: bool = None):
        """ Deprecated to use the color and is_filled as parameter."""
        if (color or is_filled) is not None:
            warnings.warn(
                "Deprecated to use the color and is_filled as parameter as they are not used. Use the set_color,"
                + "and set_filled methods to change the colors manually.")
        self.polygon.draw(drawer=drawer, outline=self.color, fill=self.is_filled)

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        self.polygon.crop(current_dim=current_dim, target_dim=target_dim, cut_left=cut_left)

    def show(self):
        """ Displays the polygon of the PageElement for debugging purposes d
        """
        # TODO: Maybe delete this method.
        centered_polygon: Polygon = Polygon(
            [(x - self.polygon.get_min_x(), y - self.polygon.get_min_x()) for x, y in self.polygon.xy])
        img_dim: ImageDimension = ImageDimension(width=centered_polygon.get_max_x(),
                                                 height=centered_polygon.get_max_y())
        img = Image.new("RGB", size=img_dim.to_tuple())
        drawer = ImageDraw.Draw(img)
        centered_polygon.draw(drawer=drawer, outline=(255, 43))
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


class DecorationElement(PageElement):
    """ The :class: `DecorationElement` class has no further characteristic than it's name. It instantiates the abstract super class
    :class: `PageElement`.
    """

    def __init__(self, polygon: Polygon):
        super().__init__(polygon)


class TextLine(PageElement):
    """ Represents all PageElements with text line characteristics. Examples are comment lines and main-text lines.
    :param polygon: represents the contour of the text line.
    :type polygon: Polygon
    :param base_line: Every :class: `TextLine` class comes with a default base_line provided by the original xml_gt.
    :type base_line: Line
    """

    @abstractmethod
    def __init__(self, base_line: Line, polygon: Polygon):
        super().__init__(polygon)
        self.base_line: Line = base_line

    def draw(self, drawer: ImageDraw, color: Tuple = None, is_filled: bool = None):
        super().draw(drawer)
        self.base_line.draw(drawer)


class MainTextLine(TextLine):
    """ The :class: `MainTextLine` class has no further characteristic than it's name. It instantiates the abstract super class
    :class: `PageElement`.
    """

    def __init__(self, base_line: Line, polygon: Polygon):
        super().__init__(base_line, polygon)


class CommentTextLine(TextLine):
    """ The :class: `CommentTextLine` class has no further characteristic than it's name. It instantiates the abstract super class
    :class: `PageElement`.
    """

    def __init__(self, base_line: Line, polygon: Polygon):
        super().__init__(base_line, polygon)


class TextLineDecoration(TextLine):
    """ Decorator class used to add further functionalities to :class: `TextLine` page elements.
    """

    @abstractmethod
    def __init__(self, text_line: TextLine, base_line: Line, polygon: Polygon):
        super().__init__(base_line, polygon)
        self.text_line: TextLine = text_line

    @abstractmethod
    def draw(self, drawer: ImageDraw, color: Tuple = None, is_filled: bool = None):
        super().draw(drawer, color, is_filled)

    @abstractmethod
    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        super().resize(current_dim, target_dim)

    @abstractmethod
    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        super().crop(current_dim, target_dim, cut_left)

    @abstractmethod
    def show(self):
        super().show()


class AscenderDescenderRegion(TextLine):
    """ Decorator of Textline which adds an x-region, ascender- and descender-region.
    :param base_line: Represents the base line of x_region.
    :param x_height: provides the distance of top line and base line.
    :type x_height: int
    :param top_line: Represents the top line of x_region.
    :type top_line: Line
    :param x_region: Denotes the region for little x.
    :type x_region: Quadrilateral
    :param ascender_region: Denotes the region of ascenders.
    :type ascender_region: Quadrilateral
    :param descender_region: Denotes the region of descenders.
    :type descender_region: Quadrilateral
    The rest of the parameters are used to give custom colors to each of the :class:`Polygon` vectorobjects.
    """

    def __init__(self, base_line: Line, polygon: Polygon, x_height: int, base_line_color: Tuple = (20, 200, 100),
                 top_line_color: Tuple = (200, 230, 20), x_region_color: Tuple = None, asc_color=(100, 22, 200),
                 desc_color=(20, 200, 200)):
        super().__init__(base_line, polygon)
        self.x_height: int = x_height
        # vector_objects
        self.top_line: Line = self._set_topline()
        self.x_region: Quadrilateral = self._set_x_region()
        self.ascender_region: Quadrilateral = self._set_ascender_region()
        self.descender_region: Quadrilateral = self._set_descender_region()
        # colors
        if x_region_color is None:
            self.x_region_color: Tuple = self.color
        else:
            self.x_region_color: Tuple = x_region_color
        self.base_line_color: Tuple = base_line_color
        self.top_line_color: Tuple = top_line_color
        self.asc_color: Tuple = asc_color
        self.desc_color: Tuple = desc_color

    def _set_topline(self):
        return Line([tuple((x, y - self.x_height)) for x, y in self.base_line.xy])

    def _set_x_region(self):
        sorted_baseline = [self.base_line.xy[1], self.base_line.xy[0]]
        top_line = self.top_line.xy
        concatenated = top_line + sorted_baseline
        return Quadrilateral(concatenated)

    def _set_ascender_region(self):
        min_x = self.polygon.get_min_x()
        min_y = self.polygon.get_min_y()
        max_x = self.polygon.get_max_x()
        region = Quadrilateral([(min_x, min_y),  # left top corner
                                (max_x, min_y),  # right top corner
                                (self.top_line.get_max_x(), self.top_line.get_max_y()),  # right bottom corner
                                (self.top_line.get_min_x(), self.top_line.get_max_y())  # left bottom corner
                                ])
        return region

    def _set_descender_region(self):
        min_x = self.polygon.get_min_x()
        max_x = self.polygon.get_max_x()
        max_y = self.polygon.get_max_y()
        region = Quadrilateral([(self.base_line.get_min_x(), self.base_line.get_min_y()),  # left top corner
                                (self.base_line.get_max_x(), self.base_line.get_min_y()),  # right top corner
                                (max_x, max_y),  # right bottom corner
                                (min_x, max_y)  # left bottom corner
                                ])
        return region

    def draw(self, drawer: ImageDraw, color: Tuple = None, is_filled: bool = None):
        super().draw(drawer, color, is_filled)
        self.top_line.draw(drawer, outline=self.top_line_color)
        self.x_region.draw(drawer,outline=self.x_region_color)
        self.ascender_region.draw(drawer, outline=self.asc_color)
        self.descender_region.draw(drawer, outline=self.desc_color)

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
        warnings.warn("The show method in asc_desc_region is not imlemented.", DeprecationWarning)


class HeadAndTailRegion(TextLine):
    pass


class Histogram(TextLine):
    pass
