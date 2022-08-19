import logging
import time
import copy
import numpy as np

from pathlib import Path
from datetime import datetime

from PIL import Image
from scipy.ndimage import gaussian_filter

from HisDB_GT_Refinement.GTRefiner.Builder.Builder_v1 import BuilderV1
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Resizer import Resizer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import sigma, truncate, RawImage


class BlurAndScaleResizerPxGT(Resizer):

    def __init__(self, target_dim: ImageDimension, algo: str):
        super().__init__(target_dim)
        self.algo = algo

    def visit_page(self, page: Page):
        # blur orig image
        img = copy.deepcopy(page.px_gt.merged_levels(all_vis=True).img_from_layer())
        # greyscale
        img.convert(mode="L")
        # blur
        raw_img = RawImage(Image.fromarray(gaussian_filter(img, sigma=sigma, truncate=truncate)))
        #raw_img = RawImage(img)
        # raw_img.img.show()
        # resize
        raw_img.resize(current_dim=page.get_img_dim(), target_dim=self.target_dim)
        raw_img.show()
        #array = raw_img.binarize(img=raw_img.img, bin_algo=self.algo)
        #img = Image.fromarray(array)
        page.px_gt.img = img
        img.show()


class BlurAndScaleResizerOrig(Resizer):

    def __init__(self, target_dim: ImageDimension, algo: str):
        super().__init__(target_dim)
        self.algo = algo

    def visit_page(self, page: Page):
        # deepcopy
        page = copy.deepcopy(page)
        # resize vector_gt
        current_dim =page.get_img_dim()
        page.vector_gt.resize(current_dim = current_dim, target_dim=self.target_dim)
        img = page.raw_img.img
        # grey scale
        img.convert(mode="L")
        # blur
        raw_img = RawImage(Image.fromarray(gaussian_filter(img, sigma=sigma, truncate=truncate)))
        #raw_img = RawImage(img)
        # resize
        raw_img.resize(current_dim=current_dim, target_dim=self.target_dim)
        # binarize
        array = raw_img.binarize(img=raw_img.img, bin_algo=self.algo)
        array = np.logical_not(array)
        img = Image.fromarray(array)
        page.vector_gt.show(img)
        img.show()
        #raw_img.show()


if __name__ == '__main__':
    start = time.time()
    now = datetime.now().strftime("%H_%M_%S")

    original = Path("../../../../CB55/img/public-test/e-codices_fmb-cb-0055_0098v_max.jpg")
    pixel = Path("../../../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0098v_max.png")
    vector_gt = Path("../../../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0098v_max.xml")
    color_table = Path("../../../Resources/ColorTables/color_table_with_color_lists.json")
    visibility_table = Path("../../../Resources/VisibilityTables/visibility_table.json")
    out_put_directory = Path("../../../Resources/NewGTs/")
    out_put_name: str = f"HisDB-GT-from-{now}"
    crop_dim: ImageDimension = ImageDimension(4500, 6000)


    target_dim: ImageDimension = ImageDimension(900, 1200)

    # build GT
    builder = BuilderV1(orig_img=original, px_gt_path=pixel, vector_gt_path=vector_gt, col_table=color_table,
                        vis_table=visibility_table)

    # # crop
    # cropper = Cropper(target_dim=crop_dim)
    # builder.crop(cropper=cropper)

    # px_gt
    # otsu_resizer = BlurAndScaleResizerPxGT(target_dim=target_dim, algo="otsu")
    # sauvola_resizer = BlurAndScaleResizerPxGT(target_dim=target_dim, algo="sauvola")
    # niblack_resizer = BlurAndScaleResizerPxGT(target_dim=target_dim, algo= "niblack")

    otsu_resizer = BlurAndScaleResizerOrig(target_dim=target_dim, algo="otsu")
    sauvola_resizer = BlurAndScaleResizerOrig(target_dim=target_dim, algo="sauvola")
    niblack_resizer = BlurAndScaleResizerOrig(target_dim=target_dim, algo= "niblack")

    builder.resize(resizer=otsu_resizer)
    builder.resize(resizer=sauvola_resizer)
    builder.resize(resizer=niblack_resizer)

    # # orig
    # otsu_resizer = BlurAndScaleResizerOrig(target_dim=target_dim, algo="otsu")
    # sauvola_resizer = BlurAndScaleResizerOrig(target_dim=target_dim, algo="sauvola")
    # niblack_resizer = BlurAndScaleResizerOrig(target_dim=target_dim, algo="niblack")
    #
    # builder.resize(resizer=otsu_resizer)
    # builder.resize(resizer=sauvola_resizer)
    # builder.resize(resizer=niblack_resizer)


    logging.info("program ended")
    end = time.time()
    logging.info("time passed: " + str(end - start))
