from __future__ import annotations
from enum import Enum
# TODO: as a client https://stackoverflow.com/questions/29503339/how-to-get-all-values-from-python-enum-class
from typing import List


class LayoutClasses(Enum):
    """
    Represents the different levels of the pixel level ground truth. Essential to the program. Must changed if further
    classes should to be added.
    """
    # Base Classes
    BACKGROUND = 1
    COMMENT = 2
    DECORATION = 4
    COMMENT_AND_DECORATION = 6
    MAINTEXT = 8
    COMMENT_AND_MAINTEXT = 10
    MAINTEXT_AND_DECORATION = 12
    MAINTEXT_AND_DECORATION_AND_COMMENT = 14
    TEXT_REGION = 255

    # Decoration Classes
    ASCENDER = 16
    XREGION = 18
    DESCENDER = 20
    BASELINE = 22
    TOPLINE = 24
    HEAD = 26
    TAIL = 28

    def __str__(self):
        """ Prettier layout than the default __str__ of Enum implementation provides."""
        return "%s: %s" % (self._name_, self._value_)

    # @classmethod
    # def get_layout_classes_containing(cls, key: str):
    #     key_as_str = str(key).upper()
    #     keys: List[LayoutClasses] = []
    #     for l_class in LayoutClasses:
    #         as_str = str(l_class._name_)
    #         if key_as_str in as_str:
    #             keys.append(l_class)
    #     return keys

    @classmethod
    def get_layout_classes_containing(cls, layout_class: LayoutClasses):
        key_as_str = str(layout_class).upper().split(":")[0]
        keys: List[LayoutClasses] = []
        for l_class in LayoutClasses:
            as_str = str(l_class._name_)
            if key_as_str in as_str:
                keys.append(l_class)
        return keys

    @classmethod
    def str_to_enum(cls, enum_name: str) -> LayoutClasses:
        for l_class in LayoutClasses:
            as_str = str(l_class._name_)
            if enum_name == as_str:
                return l_class
        raise ValueError("No such LayoutClass found: " + str(enum_name))

    def get_name(self) -> str:
        return self._name_
