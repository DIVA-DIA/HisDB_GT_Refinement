from typing import List
from copy import deepcopy
from PIL import Image, ImageDraw

from GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Polygon, Rectangle, \
    Line, Quadrilateral

if __name__ == '__main__':
    orig_img_dim: ImageDimension = ImageDimension(600, 500)
    target_dim_1: ImageDimension = ImageDimension(600, 250)
    target_dim_2: ImageDimension = ImageDimension(500, 400)

    img = Image.new("RGB", size=orig_img_dim.to_tuple())
    drawer = ImageDraw.Draw(img)

    polygon = Polygon([(200, 200), (300, 100), (500, 100), (200, 300)])
    target_polygon_1 = Polygon([(200, 100), (300, 50), (500, 50), (200, 150)])
    target_polygon_2 = Polygon([(round(200 * 5 / 6), round(200 * 4 / 5)), (round(300 * 5 / 6), round(100 * 4 / 5)),
                                (round(500 * 5 / 6), round(100 * 4 / 5)), (round(200 * 5 / 6), round(300 * 4 // 5))])
    # test __eq__
    assert polygon == polygon
    assert not target_polygon_1 == polygon
    assert not target_polygon_2 == polygon

    resized_polygon_1 = deepcopy(polygon)
    resized_polygon_1.resize(current_dim=orig_img_dim, target_dim=target_dim_1)
    resized_polygon_2 = deepcopy(polygon)
    resized_polygon_2.resize(current_dim=orig_img_dim, target_dim=target_dim_2)

    polygon.draw(drawer=drawer, fill=(255, 255, 255))
    resized_polygon_1.draw(drawer=drawer, fill=(255, 0, 0))
    resized_polygon_2.draw(drawer=drawer, fill=(0, 255, 0))

    img.show()

    # test if polygon was properly cropped
    assert resized_polygon_1 == target_polygon_1
    assert resized_polygon_2 == target_polygon_2

    print("Test successful")
