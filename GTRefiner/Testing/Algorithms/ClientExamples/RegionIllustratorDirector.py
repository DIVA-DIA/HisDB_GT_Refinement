import logging
import time
from datetime import datetime
from pathlib import Path

from PIL import Image

from HisDB_GT_Refinement.GTRefiner.Builder.Builder_v1 import BuilderV1
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Cropper import Cropper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Grouper import ThresholdGrouper, BlockGrouper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.IllustratorVisitor import Illustrator
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Sorter import DescendingSorter
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses

if __name__ == '__main__':
    start = time.time()
    now = datetime.now().strftime("%H_%M_%S")

    original = Path("../../../../CB55/img/public-test/e-codices_fmb-cb-0055_0105r_max.jpg")
    pixel = Path("../../../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0105r_max.png")
    vector_gt = Path("../../../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0105r_max.xml")
    color_table = Path("../../../Resources/ColorTables/color_table_with_color_lists.json")
    visibility_table = Path("../../../Resources/VisibilityTables/visibility_table.json")
    out_put_directory = Path("../../../Resources/NewGTs/")
    out_put_name: str = f"HisDB-GT-from-{now}"
    crop_dim: ImageDimension = ImageDimension(4500, 6000)
    target_dim: ImageDimension = ImageDimension(900, 1200)

    # build GT
    builder = BuilderV1(orig_img=original, px_gt_path=pixel, vector_gt_path=vector_gt, col_table=color_table,
                        vis_table=visibility_table)
    cropper = Cropper(target_dim=crop_dim)
    builder.crop(cropper)
    #
    # resizer = Resizer(target_dim=target_dim)
    # builder.resize(resizer=resizer)

    # make blocks base on x values
    grouper = BlockGrouper(layout_class=LayoutClasses.COMMENT)
    builder.group(grouper)
    # grouper = BlockGrouper(layout_class=LayoutClasses.DECORATION)
    # builder.group(grouper)
    # grouper = BlockGrouper(layout_class=LayoutClasses.MAINTEXT)
    # builder.group(grouper)


    sorter = DescendingSorter()
    builder.sort(sorter)
    for region in builder.page.vector_gt.regions:
        assert region._is_sorted()


    grouper = ThresholdGrouper(layout_class=LayoutClasses.COMMENT,x_threshold=300,y_threshold=300)
    builder.group(grouper)
    grouper = ThresholdGrouper(layout_class=LayoutClasses.DECORATION, x_threshold=500, y_threshold=500)
    builder.group(grouper)
    grouper = ThresholdGrouper(layout_class=LayoutClasses.MAINTEXT, x_threshold=300, y_threshold=300)
    builder.group(grouper)
    #


    illustrator = Illustrator()
    img: Image = illustrator.visit_page(builder.page)
    img.show()


    cropper = Cropper(target_dim=crop_dim)
    builder.crop(cropper)

    # builder.resize(resizer)
    # show vector objects on raw img
    # rgba_img: Image = copy.deepcopy(builder.page.raw_img.img)
    # rgba_img = rgba_img.convert("RGBA")
    # builder.page.vector_gt.show(rgba_img, color=(4,50,255,50), outline=(4,50,255,50))

    # decorator= AscenderDescenderDecorator(x_height=45)
    # builder.decorate(decorator=decorator)
    #
    # builder.set_color()
    # builder.set_visible()
    #
    # builder.page.vector_gt.show()
    #
    #
    # combiner = Combiner()
    # builder.combine(combiner=combiner)
    #
    # page: Page = builder.get_GT()
    #
    # # page.px_gt.show()
    # page.raw_img.show()
    # page.px_gt.show()
    # page.vector_gt.show()
    #
    # builder.write(output_path=Path(str(out_put_directory) + out_put_name))

    logging.info("program ended")
    end = time.time()
    logging.info("time passed: " + str(end - start))
