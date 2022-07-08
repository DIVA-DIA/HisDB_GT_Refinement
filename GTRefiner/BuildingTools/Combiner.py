from typing import Tuple

from PIL import Image

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import ColorTable


class Combiner:

    @classmethod
    def combine(cls, orig_px: PixelLevelGT, new_px_gt: PixelLevelGT) -> Image:
        """ Overlays and colors the visible layers of the new pixel ground truth (generated from the vector ground
        truth) with the original pixel level ground truth and return a single image.
        """
        assert new_px_gt.img_dim == orig_px.img_dim
        img_dim = orig_px.img_dim
        output_img: Image = Image.new("RGB", img_dim.to_tuple())
        # paint
        for k, v in new_px_gt.levels.items():
            temp_img = Image.new("RGB", img_dim.to_tuple())
            if v.visible is True:
                base_layer = Layer(img_dim=img_dim)
                # handle the case of ascenders & descenders
                if (k is LayoutClasses.ASCENDER) or (k is LayoutClasses.XREGION) or (k is LayoutClasses.DESCENDER):
                    # get all textline classes
                    target_classes = LayoutClasses.get_layout_classes_containing(LayoutClasses.MAINTEXT)
                    target_classes.extend(LayoutClasses.get_layout_classes_containing(LayoutClasses.COMMENT))
                    for l_class in target_classes:
                        base_layer: Layer = base_layer.unite(orig_px[l_class])
                    base_layer: Layer = base_layer.intersect(v)
                else:
                    base_layer = base_layer.unite(orig_px[k])
                    base_layer: Layer = base_layer.intersect(v)
                # merge the two layers.
                output_img: Image = base_layer.paint_layer_on_img(output_img)
        return output_img






