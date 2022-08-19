from PIL import Image

from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import Visitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer


# Layerer successfully draws maintext, comments and decorations on the px_gt. However, it's difficult for the layerer to
# get to decorators. Thus I will implement a layer method (like the draw) for every leaf of PageElements. This way I
# won't have to care about traversing the the tree structure.


class Combiner(Visitor):
    """Combiner combines information from both ground truths (vector gt and pixel-based gt)."""

    @classmethod
    def visit_page(cls, page: Page):
        """The default implementation of Combiner combines the vector gt and pixel gt by drawing the vector objects on
        the according layer of the levels within the pixel gt. It takes use of the Layarable :class: `Layerable` interface.
        :param page:
        :type page:
        :return:
        :rtype:
        """
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
