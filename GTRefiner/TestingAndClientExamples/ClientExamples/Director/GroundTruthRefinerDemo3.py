import json
import logging
import time
from datetime import datetime
from pathlib import Path
from PIL import Image

from HisDB_GT_Refinement.GTRefiner.Builder.Builder_v1 import BuilderV1
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Cropper import Cropper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Grouper import ThresholdGrouper, BlockGrouper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.IllustratorVisitor import Illustrator
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Layerer import Layerer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Resizer import Resizer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Sorter import DescendingSorter
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page

# This is an example for a Ground-Truth-Director. It takes use of the Ground-Truth Builder Module and it's crop(),
# resize() and decorate() functions to design the target Ground-Truth with ascenders and descenders. Furthermore it groups
# the comments into blocks.
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import ColorTable, VisibilityTable

col_table_demo_3 = ColorTable({'BACKGROUND': [[0, 0, 0]],
                               'COMMENT': [[177, 50, 255], [255, 50, 177], [50, 255, 177]],
                               'DECORATION': [[55, 88, 200]],
                               'COMMENT_AND_DECORATION': [[255, 255, 0]],
                               'MAINTEXT': [[255, 200, 20], [255, 200, 40], [255, 200, 60], [255, 200, 80],
                                            [255, 200, 100], [255, 200, 120], [255, 200, 140], [255, 200, 160],
                                            [255, 200, 180], [255, 200, 200]],
                               'COMMENT_AND_MAINTEXT': [[255, 0, 255]],
                               'MAINTEXT_AND_DECORATION': [[0, 255, 255]],
                               'MAINTEXT_AND_DECORATION_AND_COMMENT': [[255, 255, 255]],
                               'ASCENDER': [[250, 120, 23]],
                               'XREGION': [[30, 250, 120]],
                               'DESCENDER': [[120, 20, 250]],
                               'BASELINE': [[30, 100, 200]],
                               'TOPLINE': [[100, 30, 200]],
                               'TEXT_REGION': [[100, 100, 0], [100, 100, 50], [100, 100, 100], [100, 100, 150],
                                               [100, 100, 200], [100, 100, 250]]
                               })
vis_table_demo_3 = VisibilityTable({LayoutClasses.MAINTEXT: False,
                                    LayoutClasses.COMMENT: True,
                                    LayoutClasses.DECORATION: False,
                                    LayoutClasses.ASCENDER: False,
                                    LayoutClasses.DESCENDER: True,
                                    LayoutClasses.TEXT_REGION: True,
                                    LayoutClasses.MAINTEXT_AND_DECORATION_AND_COMMENT: False,
                                    LayoutClasses.MAINTEXT_AND_DECORATION: False,
                                    LayoutClasses.COMMENT_AND_MAINTEXT: False,
                                    LayoutClasses.COMMENT_AND_DECORATION: False,
                                    LayoutClasses.XREGION: False,
                                    LayoutClasses.BASELINE: False,
                                    LayoutClasses.BACKGROUND: False})

if __name__ == '__main__':
    start = time.time()
    now = datetime.now().strftime("%H_%M_%S")

    # original ground-truth
    original = Path("../../../../CB55/img/public-test/e-codices_fmb-cb-0055_0105r_max.jpg")
    pixel = Path("../../../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0105r_max.png")
    vector_gt = Path("../../../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0105r_max.xml")

    # rules for coloring and visibility
    color_table = Path("../../../Resources/ColorTables/color_table_for_demo_2_v2.json")
    visibility_table = Path("../../../Resources/VisibilityTables/visibility_table.json")

    # output-directory
    out_put_directory = Path("../../../Resources/NewGTs/Demo/Demo2ForPresentation/")
    out_put_name: str = f"Demo-For-Presenation-3-{now}"

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

    # # you can illustrate if it is correctly cropped and scaled
    # builder.page.vector_gt.show(builder.page.px_gt.merged_levels(all_vis=True).img_from_layer(rgb=True))

    # set the colors and visibility
    builder.set_color()
    builder.set_visible()

    # sort the ground-truth elements
    sorter = DescendingSorter()
    builder.sort(sorter)

    for region in builder.page.vector_gt.regions:
        assert region._is_sorted()

    # make blocks base on x values
    grouper = BlockGrouper(layout_class=LayoutClasses.COMMENT)
    builder.group(grouper)
    # grouper = BlockGrouper(layout_class=LayoutClasses.DECORATION)
    # builder.group(grouper)
    # grouper = BlockGrouper(layout_class=LayoutClasses.MAINTEXT)
    # builder.group(grouper)

    # group based on a given threshold
    grouper = ThresholdGrouper(layout_class=LayoutClasses.COMMENT, x_threshold=80, y_threshold=80)
    builder.group(grouper)
    # grouper = ThresholdGrouper(layout_class=LayoutClasses.DECORATION, x_threshold=500, y_threshold=500)
    # builder.group(grouper)
    # grouper = ThresholdGrouper(layout_class=LayoutClasses.MAINTEXT, x_threshold=300, y_threshold=300)
    # builder.group(grouper)

    illustrator = Illustrator(background=builder.page.vector_gt.show(), color_table=col_table_demo_3)
    img: Image = illustrator.visit_page(builder.page)
    img.show()

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
