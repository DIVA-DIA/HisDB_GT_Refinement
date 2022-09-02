import json
import logging
import time
from datetime import datetime
from pathlib import Path

from HisDB_GT_Refinement.GTRefiner.Builder.Builder_v1 import BuilderV1
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Layerer import Layerer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Cropper import Cropper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Resizer import Resizer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.TextLineDecorator import AscenderDescenderDecorator
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page

# This is an example for a Ground-Truth-Director. It takes use of the Ground-Truth Builder Module and it's crop(),
# resize() and decorate() functions to design the target Ground-Truth with ascenders and descenders.
# All layout classes should be visible.

col_table_demo_1 = {'BACKGROUND': [[0, 0, 0]],
                    'COMMENT': [[177, 50, 80]],
                    'DECORATION': [[45, 200, 20]],
                    'COMMENT_AND_DECORATION': [[255, 255, 0]],
                    'MAINTEXT': [[55, 88, 200]],
                    'COMMENT_AND_MAINTEXT': [[255, 0, 255]],
                    'MAINTEXT_AND_DECORATION': [[0, 255, 255]],
                    'MAINTEXT_AND_DECORATION_AND_COMMENT': [[255, 255, 255]],
                    'ASCENDER': [[250, 120, 23]],
                    'XREGION': [[30, 250, 120]],
                    'DESCENDER': [[120, 20, 250]],
                    'BASELINE': [[30, 100, 200]],
                    'TOPLINE': [[100, 30, 200]],
                    'TEXT_REGION': [[100, 100, 100]]}

if __name__ == '__main__':
    start = time.time()
    now = datetime.now().strftime("%H_%M_%S")

    # original ground-truth
    original = Path("../../../../CB55/img/public-test/e-codices_fmb-cb-0055_0098v_max.jpg")
    pixel = Path("../../../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0098v_max.png")
    vector_gt = Path("../../../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0098v_max.xml")

    # rules for coloring and visibility
    color_table = Path("../../../Resources/ColorTables/color_table_for_demo.json")
    visibility_table = Path("../../../Resources/VisibilityTables/visibility_table.json")

    # output-directory
    out_put_directory = Path("../../../Resources/NewGTs/DemoForPresentation/")
    out_put_name: str = f"Demo-For-Presenation-{now}"

    # target dimension
    crop_dim: ImageDimension = ImageDimension(4500, 6000)
    target_dim: ImageDimension = ImageDimension(900, 1200)

    # initialisation of the builder
    builder = BuilderV1(orig_img=original, px_gt_path=pixel, vector_gt_path=vector_gt, col_table=color_table,
                        vis_table=visibility_table)

    # cropping
    cropper = Cropper(target_dim=crop_dim)
    builder.crop(cropper)

    # resizing
    resizer = Resizer(target_dim=target_dim)
    builder.resize(resizer)

    # # you can test if it is correctly cropped and scaled
    # builder.page.vector_gt.show(builder.page.px_gt.merged_levels(all_vis=True).img_from_layer(rgb=True))

    # decorate
    decorator = AscenderDescenderDecorator(x_height=10)
    builder.decorate(decorator=decorator)

    # set the colors and visibility
    builder.set_color()
    builder.set_visible()

    # combine the two ground-truths to one pixel-ground-truth
    layerer = Layerer()
    builder.layer(layerer=layerer)

    # get the final page
    page: Page = builder.get_GT()

    # illustrate the page
    page.raw_img.show()
    page.px_gt.show()
    page.vector_gt.show()

    # write the page to the output directory
    builder.write(output_path=Path(str(out_put_directory) + out_put_name))

    logging.info("program ended")
    end = time.time()
    logging.info("time passed: " + str(end - start))
