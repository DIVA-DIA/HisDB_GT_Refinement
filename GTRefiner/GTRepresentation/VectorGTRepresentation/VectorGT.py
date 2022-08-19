from typing import Dict, List, Tuple

import numpy as np
from PIL import Image
from PIL import ImageDraw

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import GroundTruth
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Dictionable, Scalable, Croppable, \
    Drawable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import TextRegion, ImageDimension


class VectorGT(GroundTruth, Dictionable, Scalable, Croppable, Drawable):

    def __init__(self, regions: List[TextRegion], img_dim: ImageDimension):
        super().__init__(img_dim)
        self.regions: List[TextRegion] = regions

    def get_dim(self):
        """
        :return: Return the dimension of this vector_gt
        :rtype: ImageDimension
        """
        return super().get_dim()

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        """Resizes all page elements :class: `List[PageElement]` of the current :class: `LayoutClass` to a given target
        dimension. As this class doesn't possess a image dimension parameter, both the current dimension (of the page)
        and the target dimension (the size to be scaled to) must be given.
        :param current_dim: Current dimension
        :type current_dim: ImageDimension
        :param target_dim: Target dimension
        :type target_dim: ImageDimension
        """
        for layout in self.regions:
            for region in layout.text_regions:
                for elem in region.page_elements:
                    elem.resize(current_dim=current_dim, target_dim=target_dim)
        self.img_dim = target_dim

    def show(self, base_img: Image = None, transparency=0.5, color: Tuple = None, outline: Tuple = None):
        """ Illustrate the vector ground truth according to the clients needs (especially useful for debugging).
        :param base_img: If given, this image will be the base image where the vector objects are drawn upon.
        :type base_img: Image
        :param transparency: The factor to which the layers should be overlayed. A value smaller than 0.5 prioritizes
        the base img. A value bigger than 05. prioritizes the vector objects.
        :type transparency: int
        :param color: color the page elements should be drawn in. We suggest you use a color table and :class: `Colorer`
        to color the elements individually.
        :type color: tuple
        :param outline: Outline of the vector objects to be drawn (illustrated).
        :type outline: tuple
        :return:
        :rtype:
        """
        drawn_vector_objects = Image.new("RGB", size=self.img_dim.to_tuple())
        drawer = ImageDraw.Draw(drawn_vector_objects)
        for layout in self.regions:
            for region in layout.text_regions:
                for elem in region.page_elements:
                    elem.draw(drawer=drawer, color=color, outline=outline)
                    # drawn_vector_objects.show() # debug
        if base_img:
            base_img = base_img.convert("RGB")
            drawn_vector_objects = Image.blend(drawn_vector_objects, base_img, transparency)
        drawn_vector_objects.show()

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        """Crop all page elements of this vector gt to a target dimension. Due to the nature of the ground truth document
        :param cut_left: must be provided.
        :param current_dim: Current dimension
        :type current_dim: ImageDimension
        :param target_dim: Target dimension
        :type target_dim: ImageDimension
        :param cut_left: Whether or not the page is cut_left or not.
        :type cut_left: bool
        """
        for layout in self.regions:
            for region in layout.text_regions:
                for elem in region.page_elements:
                    elem.crop(current_dim=current_dim, target_dim=target_dim, cut_left=cut_left)
        self.img_dim = target_dim

    def build(self) -> Dict:
        global_dict = {"ImageDimension": self.img_dim.to_tuple()}
        dict = {}
        for i, region in enumerate(self.regions):
            region_dict = {}
            region_dict.update(region.build())
            dict[type(region).__name__ + " " + str(i)] = region_dict
        global_dict["Vector Ground Truth"] = dict
        return global_dict

    def layer(self, img):
        """Draw all visible page_elements of all visible layers of all visible regions on an image."""
        for text_region in self.regions:
            img = text_region.layer(img)
        return img

    def __eq__(self, other):
        if not type(other) is type(self):
            return False
        img_1 = Image.new("RGB", size=self.img_dim.to_tuple())
        drawer_1 = ImageDraw.Draw(img_1)
        for layout in self.regions:
            for region in layout.text_regions:
                for elem in region.page_elements:
                    elem.draw(drawer=drawer_1)
        img_as_array_1 = np.asarray(img_1)

        img_2 = Image.new("RGB", size=other.img_dim.to_tuple())
        drawer_2 = ImageDraw.Draw(img_2)
        for layout in other.regions:
            for region in layout.text_regions:
                for elem in region.page_elements:
                    elem.draw(drawer=drawer_2)
        img_as_array_2 = np.asarray(img_2)
        # for debugging
        # what_is_missing = np.logical_xor(img_as_array_1,img_as_array_2)
        # what_is_missing = np.where(what_is_missing,255,0)
        # img = Image.fromarray(what_is_missing.astype("uint8"))
        # img.show()
        return (img_as_array_1 == img_as_array_2).all()

    def draw(self, drawer: ImageDraw, color: Tuple = None, outline=None):
        """For all visible layouts and pagelements, draw them on given image in a certain color and
        outline.
        TODO: What's the difference of this method to the layer method?
        :param drawer: image to be drawn upon.
        :type drawer: ImageDraw.ImageDraw
        :param color: fill of the object. Can be of any mode that pillow understands (e.g. RGBA, 1, L, RGB).
        :type color: tuple
        :param outline: outline of the object. Should only be used for illustration purposes!
        Can be of any mode that pillow understands (e.g. RGBA, 1, L, RGB).
        :type outline: tuple"""
        for region in self.regions:
            for layout in region.text_regions:
                layout.draw(drawer=drawer, color=color, outline=outline)
