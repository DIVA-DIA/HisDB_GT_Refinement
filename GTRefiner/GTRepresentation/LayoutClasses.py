from enum import Enum

# TODO: as a client https://stackoverflow.com/questions/29503339/how-to-get-all-values-from-python-enum-class
class LayoutClasses(Enum):
    """
    Represents the different classes of the pixel ground truth. Essential to the program. Must changed if further
    classes should to be added.
    """
    BACKGROUND = 1
    COMMENT = 2
    DECORATION = 4
    COMMENT_AND_DECORATION = 6
    MAINTEXT = 8
    COMMENT_AND_MAINTEXT = 10
    MAINTEXT_AND_DECORATION = 12
    MAINTEXT_AND_DECORATION_AND_COMMENT = 14
    ASCENDER = 16
    XREGION = 18
    DESCENDER = 20
    HEAD = 22
    TAIL = 24
    TEXT_REGIONS = 255

    def __str__(self):
        """ Prettier layout than the default __str__ of Enum implementation provides."""
        return "%s: %s" % (self._name_, self._value_)