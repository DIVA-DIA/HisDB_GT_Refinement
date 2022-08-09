import logging
import time

from pathlib import Path
from datetime import datetime
from HisDB_GT_Refinement.GTRefiner.Builder.Builder_v1 import BuilderV1
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Colorer import Colorer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Combiner import Combiner
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Cropper import Cropper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Resizer import Resizer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.TextLineDecorator import AscenderDescenderDecorator
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page

if __name__ == '__main__':
    start = time.time()
    now = datetime.now().strftime("%H_%M_%S")

    original = Path("../../CB55/img/public-test/e-codices_fmb-cb-0055_0098v_max.jpg")
    pixel = Path("../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0098v_max.png")
    vector_gt = Path("../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0098v_max.xml")
    color_table = Path("../Resources/ColorTables/color_table_with_color_lists_2.json")
    visibility_table = Path("../Resources/VisibilityTables/visibility_table.json")
    out_put_directory = Path("../Resources/NewGTs/")
    out_put_name: str = f"HisDB-GT-from-{now}"
    crop_dim: ImageDimension = ImageDimension(4500, 6000)
    target_dim: ImageDimension = ImageDimension(900, 1200)

    # build GT
    builder = BuilderV1(orig_img=original, px_gt_path=pixel, vector_gt_path=vector_gt, col_table=color_table, vis_table=visibility_table)

    cropper = Cropper(target_dim=crop_dim)
    builder.crop(cropper)

    resizer = Resizer(target_dim=target_dim)
    builder.resize(resizer)
    # test if correctly cropped and scaled
    builder.page.vector_gt.show(builder.page.px_gt.merged_levels(all_vis=True).img_from_layer(rgb=True))

    decorator= AscenderDescenderDecorator(x_height=12)
    builder.decorate(decorator=decorator)

    builder.set_color()
    builder.set_visible()

    builder.page.vector_gt.show()


    combiner = Combiner()
    builder.combine(combiner=combiner)

    page: Page = builder.get_GT()

    # page.px_gt.show()
    page.raw_img.show()
    page.px_gt.show()
    page.vector_gt.show()

    builder.write(output_path=Path(str(out_put_directory) + out_put_name))

    logging.info("program ended")
    end = time.time()
    logging.info("time passed: " + str(end - start))


