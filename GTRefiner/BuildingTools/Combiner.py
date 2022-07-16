from abc import abstractmethod
from typing import List

from PIL import Image

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
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


class Combiner():

    @classmethod
    def construct(cls, page: Page):
        _layered_img = cls._layer(page)
        _combined_img = cls._combine(page, _layered_img)

    @classmethod
    def _layer(cls, page: Page) -> Image:
        img: Image = Image.new("RGB", size=page.vector_gt.get_dim().to_tuple())
        return page.vector_gt.layer(img)

    @classmethod
    def _combine(cls, page: Page, layered_img: Image) -> Image:
        bin_mask_from_layered_img: Layer = Layer.bin_layer_from_rgb(layered_img)
        intersected_mask: Layer = bin_mask_from_layered_img.intersect(
            page.px_gt.merged_levels(all_vis=True))
        # debugging
        intersected_mask.show()
        layered_img.show()

        final: Image = intersected_mask.intersect_this_layer_with_an_rgb_img(layered_img)
        final.show()
        page.px_gt.img = final
