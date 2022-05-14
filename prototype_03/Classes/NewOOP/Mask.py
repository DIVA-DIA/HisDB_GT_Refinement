# this script provides classes for masking and combining of masks
from typing import Tuple, List
import numpy as np
from PIL import Image
from abc import abstractmethod

from PIL.ImageDraw import ImageDraw

#from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.MaskingStrategy import Masker
from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.Scalable import Scalable
from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.Textline import MainText, CommentText
from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.VectorObject import VectorObject, Polygon, Box, BoundingBox


# TODO: should I write masks for every application? -> E.g. PolygonAscDescMask? In other words what kind of Masks do I need?

class Mask(Scalable):
    # Masks must be binary
    mode = "1"
    shape = (6496,4872)

    def __init__(self, mask: np.ndarray = None):
        if mask is None:
            self._initialize_mask()
        else:
            self.mask = mask

    def _initialize_mask(self):
        self.mask = np.zeros(shape=self.shape, dtype=bool)

    def show(self):
        """
        Display the image
        """
        img = self.img_from_mask()
        img.show()

    def img_from_mask(self):
        """
        Return a binary image from it's mask
        :return: Image
        """
        return Image.fromarray(obj=self.mask)

    def resize(self, size: Tuple):
        pass


# For polygons, rectangles, etc.
class ShapeMask(Mask):

    def __init__(self, vector_obj: VectorObject, mask: np.ndarray = None):
        super().__init__(mask)
        self.vector_obj = vector_obj
        self.mask = self.make_mask(vector_obj=vector_obj)

    def make_mask(self, vector_obj: VectorObject):
        img = self.img_from_mask()
        drawer = ImageDraw(im=img, mode=self.mode)
        vector_obj.draw(drawer=drawer, outline=1, fill=1)
        img_as_array = np.asarray(img)
        return img_as_array


class Masker:
    # TODO: make return type same as input type
    def union(self, mask1: Mask, mask2: Mask) -> Mask:
        assert mask1.mask.shape == mask2.mask.shape
        return Mask(np.bitwise_or(mask1.mask, mask2.mask))

    def intersection(self, mask1: Mask, mask2: Mask) -> Mask:
        assert mask1.mask.shape == mask2.mask.shape
        return Mask(np.bitwise_xor(mask1.mask, mask2.mask))

    def invert(self, mask: Mask) -> Mask:
        return Mask(np.invert(mask.mask))

    @abstractmethod
    def mask(self) -> Mask:
        pass


# extends the mask, holds a masker
class TextLineMask(Mask):

    def __init__(self, main_text: MainText, comments: CommentText):
        self._main_text: MainText = main_text
        self._comments: CommentText = comments
        super().__init__()
        self._initialize_mask()

    def _initialize_mask(self):
        global_mask: Mask = Mask()
        masker = Masker()
        for textlines in self._main_text:
            polygon: Polygon = textlines.polygon
            temp_mask: Mask = masker.union(mask1=ShapeMask(polygon), mask2=global_mask)
            global_mask = masker.union(global_mask, temp_mask)

        for comments in self._comments:
            polygon: Polygon = comments.polygon
            temp_mask: Mask = masker.union(mask1=ShapeMask(polygon), mask2=global_mask)
            global_mask = masker.union(global_mask, temp_mask)
        self.mask = global_mask.mask

class ASC_DESC_Mask(Mask):

    def __init__(self, main_text: MainText, comments: CommentText):
        self._main_text: MainText = main_text
        self._comments: CommentText = comments
        super().__init__()
        self._initialize_mask()

    def _initialize_mask(self):
        global_mask: Mask = Mask()
        masker = Masker()
        for textlines in self._main_text:
            polygon: Polygon = textlines.polygon
            temp_mask: Mask = masker.union(mask1=ShapeMask(polygon), mask2=global_mask)
            asc_mask: Mask = masker.union()
            global_mask = masker.union(global_mask, temp_mask)

        for comments in self._comments:
            polygon: Polygon = comments.polygon
            temp_mask: Mask = masker.union(mask1=ShapeMask(polygon), mask2=global_mask)
            global_mask = masker.union(global_mask, temp_mask)
        self.mask = global_mask.mask





if __name__ == '__main__':
    shape = (800, 800)

    polygon_1 = [(15, 25), (100, 50), (250, 8), (256, 360), (200, 310), (50, 103)]
    vector_object_1 = Polygon(polygon=polygon_1)

    polygon_2 = [(75, 25), (150, 90), (300, 80), (305, 250), (100, 260), (10, 277)]
    vector_object_2 = Polygon(polygon=polygon_2)

    mask_1 = ShapeMask(vector_obj=vector_object_1)
    mask_2 = ShapeMask(vector_obj=vector_object_2)

    masker = Masker()

    union_result = masker.union(mask1=mask_1, mask2=mask_2)
    intersection_result = mask=masker.intersection(mask1=mask_1, mask2=mask_2)

    text_line_masker: Masker = TextLineMasker(Polygon(polygon_1), BoundingBox(polygon_1))
    text_line_mask: Mask = text_line_masker.mask()

    #mask_1.show()
    #mask_2.show()
    union_result.show()

    #union_result.show()
    #intersection_result.show()
