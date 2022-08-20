from pathlib import Path
from typing import List

from PIL import Image, ImageDraw

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Polygon, Rectangle, \
    Line, Quadrilateral
from HisDB_GT_Refinement.GTRefiner.IO.Reader import XMLReader


def test_basic_quadr_instanciation():
    orig_img_dim: ImageDimension = ImageDimension(600, 500)
    target_dim: ImageDimension = ImageDimension(500, 400)

    img = Image.new("RGB", size=orig_img_dim.to_tuple())
    drawer = ImageDraw.Draw(img)

    polygon = Polygon([(100,40), (110,95), (50,50), (50,100)])
    # target_polygon = Polygon([(100, 150), (200, 50), (400, 50), (100, 250)])

    sorted_quadr: Quadrilateral = Quadrilateral([(50,50),(100,40), (110,95), (50,100)])
    un_sorted_quadr_1:Quadrilateral = Quadrilateral([(100,40), (110,95), (50,50), (50,100)])
    un_sorted_quadr_2:Quadrilateral = Quadrilateral([(100, 40), (110, 95), (50,100), (50, 50)])


    # test __eq__
    assert un_sorted_quadr_1 == sorted_quadr
    assert un_sorted_quadr_2 == sorted_quadr

    assert sorted_quadr.is_sorted()

    sorted_quadr.draw(drawer=drawer, color=(255, 255, 255))
    un_sorted_quadr_1.draw(drawer=drawer, color=(255, 0, 0))
    un_sorted_quadr_2.draw(drawer=drawer, color=(0, 100, 255))

    img.show()

    print("Test successful")

if __name__ == '__main__':

    test_basic_quadr_instanciation()

    # # test vector_gt
    # vector_gt_path = Path("../../../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0105r_max.xml")
    # vector_gt: VectorGT = XMLReader.read(path=vector_gt_path)
    # vector_gt.show()


