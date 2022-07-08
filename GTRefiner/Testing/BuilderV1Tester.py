import logging
import time
from pathlib import Path

from HisDB_GT_Refinement.GTRefiner.Builder.Builder_v1 import BuilderV1
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Combiner import Combiner
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT

if __name__ == '__main__':
    start = time.time()


    original = Path("../../CB55/img/public-test/e-codices_fmb-cb-0055_0105r_max.jpg")
    pixel = Path("../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0105r_max.png")
    vector_gt = Path("../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0105r_max.xml")

    builder = BuilderV1(orig_img=original,px_gt_path=pixel, vector_gt_path=vector_gt)

    target_dim: ImageDimension = ImageDimension(4500, 6000)
    builder.crop(target_dim)

    # TODO: Frage an Lars. Was ist praktisch als client. Wie viel responsibilities soll er kriegen. Soll der Client vor
    #  allem den Director oder auch den Builder selber schreiben...

    target_dim: ImageDimension = ImageDimension(1800, 2400)
    builder.resize(target_dim=target_dim)

    builder.decorate()

    builder.set_visible()

    new_px_gt: PixelLevelGT = builder.layer()

    combiner = Combiner()
    builder.combine_px_gts(combiner)

    builder.write(None)

    page: Page = builder.get_GT()

    #page.px_gt.show()

    logging.info("program ended")
    end = time.time()
    logging.info("time passed: " + str(end - start))