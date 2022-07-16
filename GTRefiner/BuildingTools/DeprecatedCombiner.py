# import logging
# import time
# from typing import Tuple
# import warnings
# import numpy as np
# from PIL import Image
#
# from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
# from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
# from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT
# from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import ColorTable
#
# logging.getLogger().setLevel(logging.INFO)
#
# class Combiner:
#
#     @classmethod
#     def combine(cls, orig_px: PixelLevelGT, new_px_gt: PixelLevelGT) -> Image:
#         """ Overlays and colors the visible layers of the new pixel ground truth (generated from the vector ground
#         truth) with the original pixel level ground truth and return a single image.
#         """
#         # create new image to paint on
#         assert new_px_gt.img_dim == orig_px.img_dim
#         img_dim = orig_px.img_dim
#         output_img: Image = Image.new("RGB", img_dim.to_tuple())
#         # paint
#         for k, v in orig_px.levels.items():
#             if v.visible is True:
#                 base_layer = Layer(img_dim=img_dim)
#                 # handle the case of ascenders & descenders
#                 if (k is LayoutClasses.ASCENDER):
#                     # get all textline classes
#                     target_classes = LayoutClasses.get_layout_classes_containing(LayoutClasses.MAINTEXT)
#                     target_classes.extend(LayoutClasses.get_layout_classes_containing(LayoutClasses.COMMENT))
#                     orig_comments_and_maintext = Layer(img_dim=img_dim)
#                     for l_class in target_classes:
#                         orig_comments_and_maintext = orig_comments_and_maintext.unite(orig_px[l_class])
#                         base_layer = base_layer.unite(new_px_gt[l_class])
#                     if np.any(base_layer.layer) == False:
#                         warnings.warn("Base Layer is empty after unite() Key = " + str(k))
#                     base_layer = base_layer.intersect(orig_comments_and_maintext)
#                     if np.any(base_layer.layer) == False:
#                         warnings.warn("Base Layer is empty after intersect() Key = " + str(k))
#                 else:
#                     base_layer = base_layer.unite(new_px_gt[k])
#                     if np.any(base_layer.layer) == False:
#                         warnings.warn("Base Layer is empty after unite() Key = " + str(k))
#                     base_layer = base_layer.intersect(v)
#                     if np.any(base_layer.layer) == False:
#                         warnings.warn("Base Layer is empty after intersect() Key = " + str(k))
#                 # merge the two layers.
#                 output_img: Image = base_layer.paint_layer_on_img(output_img, color=v.color)
#             output_img.show()
#         return output_img
#
#
#
#
#
#
