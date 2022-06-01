from enum import Enum


class LayoutClasses(Enum):
    """
    Represents the different classes of the pixel ground truth. Is useful for readability and implementation of
    Layering.
    """
    BACKGROUND = 1
    COMMENT = 2
    DECORATION = 4
    COMMENT_AND_DECORATION = 6
    MAINTEXT = 8
    COMMENT_AND_MAINTEXT = 10
    MAINTEXT_AND_DECORATION = 12
    MAINTEXT_AND_DECORATION_AND_COMMENT = 14
    TEXT_REGIONS = 255

    def __str__(self):
        """ Prettier layout than the default __str__ of Enum implementation provides."""
        return "%s: %s" % (self._name_, self._value_)