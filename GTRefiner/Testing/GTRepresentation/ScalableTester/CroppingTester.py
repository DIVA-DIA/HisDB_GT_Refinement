from typing import List

from PIL import Image, ImageDraw

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Polygon, Rectangle, \
    Line, Quadrilateral

if __name__ == '__main__':
    orig_img_dim: ImageDimension = ImageDimension(600, 500)
    target_dim: ImageDimension = ImageDimension(500, 400)

    img = Image.new("RGB", size=orig_img_dim.to_tuple())
    drawer = ImageDraw.Draw(img)

    polygon = Polygon([(200, 200), (300, 100), (500, 100), (200, 300)])
    target_polygon = Polygon([(100, 150), (200, 50), (400, 50), (100, 250)])

    # test __eq__
    assert polygon == polygon
    assert not target_polygon == polygon

    polygon.crop(current_dim=orig_img_dim, target_dim=target_dim, cut_left=True)

    polygon.draw(drawer=drawer, fill=(255, 255, 255))
    target_polygon.draw(drawer=drawer, fill=(255, 0, 0))

    img.show()

    # test if polygon was properly cropped
    assert polygon == target_polygon

    print("Test successful")
