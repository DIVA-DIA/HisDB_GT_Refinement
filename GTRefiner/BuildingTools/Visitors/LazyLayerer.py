from abc import abstractmethod
from typing import List

from PIL import Image

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import PageElement
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import LayoutVisitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import Decorations, CommentText, \
    MainText, Layout


# Layerer successfully draws maintext, comments and decorations on the px_gt. However, it's difficult for the layerer to
# get to decorators. Thus I will implement a layer method (like the draw) for every leaf of PageElements. This way I
# won't have to care about traversing the the tree structure.


class Layerer():

    def __init__(self, vector_gt: VectorGT, px_gt: PixelLevelGT):
        self._px_gt: PixelLevelGT = px_gt
        self._vector_gt: VectorGT = vector_gt
        self._layered_img: Image = self.layer(Image.new("RGB", size=vector_gt.get_dim().to_tuple()))
        self._combined_img: Image = self.combine()

    def layer(self, img: Image) -> Image:
        return self._vector_gt.layer(img)

    def combine(self) -> Image:
        bin_mask_from_layered_img: Layer = Layer.bin_layer_from_rgb(self._layered_img)
        intersected_mask: Layer = bin_mask_from_layered_img.intersect(
            self._px_gt.merged_levels(all_vis=True))
        # debugging
        intersected_mask.show()
        self._layered_img.show()
        final: Image = intersected_mask.intersect_this_layer_with_an_rgb_img(self._layered_img)
        final.show()
        return final