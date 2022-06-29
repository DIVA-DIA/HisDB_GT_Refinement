from __future__ import annotations
from abc import abstractmethod
from typing import List, Tuple

from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.GT_Buildingblocks.PageElements import PageElement


class Block():
    """ The Block class' purpose is to group PageElements (maintext, comments, decoractions) according to a given logic
    (e.g. into paragraphs for maintext or different comment blocks for comments). Blocks is a trivial implementation
    and can be extended for desired characteristics."""
    def __init__(self):
        self.page_elements: List[PageElement] = []
        self._set_region()
        self._x_threshold: int = 0 # if not changed by the set_threshold function, the grouping function won't change anything
        self._y_threshold: int = 0

    @abstractmethod
    def sort(self):
        pass

    @abstractmethod
    def group(self):
        """
        Group
        :return:
        """
        pass

    def merge(self, block: Block):
        """
        Merges block with another one.
        :param block: other Block
        :return: None
        """
        self.page_elements = self.page_elements + block.page_elements

    def _set_region(self):
        """ Creates a bounding box for the block"""
        min_x = float("inf")
        max_x = 0
        min_y = float("inf")
        max_y = 0
        for elem in self.page_elements:
            for coord in elem.polygon:
                if coord[0] < min_x:
                    min_x = int(coord[0])
                elif coord[0] > max_x:
                    max_x = int(coord[0])
                if coord[1] < min_y:
                    min_y = int(coord[1])
                elif coord[1] > max_y:
                    max_y = int(coord[1])
        assert min_x and max_x and min_y and max_y is not None
        assert (min_x <= max_x) and (min_y <= max_y)
        return [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]



