import logging
import time
from pathlib import Path

from HisDB_GT_Refinement.GTRefiner.Builder.Builder_v1 import BuilderV1
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import *
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import *
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Polygon
from HisDB_GT_Refinement.GTRefiner.IO.Reader import ColorTableReader


def center_polygon(polygon: Polygon, min_x=None, min_y=None):
    if min_x is None:
        min_x = polygon.get_min_x()
        min_y = polygon.get_min_y()
    else:
        min_x = min_x
        min_y = min_y
    return Polygon([(x - min_x, y - min_y) for x, y in polygon.xy]), min_x, min_y


def test_merge_and_draw():
    img_dim = ImageDimension(100, 100)
    img: Image = Image.new("RGB", size=img_dim.to_tuple())
    img_drawer = ImageDraw(img)
    layers: List[Layer] = []
    # base_layer
    base_quad: Quadrilateral = Quadrilateral([(0, 50), (50, 0), (100, 50), (50, 100)])
    base_layer: Layer = Layer(img_dim=img_dim, color=(255, 100, 50))
    layers.append(base_layer)
    base_layer.draw(base_quad)
    base_layer.show()
    # # test if layers with only one element is drawn -> test successful
    # img_from_one_layer = Layer.merge_and_draw(layers=layers, img = img)
    # img_from_one_layer.show()
    # next_layer
    next_shape: Quadrilateral = Quadrilateral([(0, 0), (100, 0), (100, 50), (0, 50)])
    next_layer: Layer = Layer(img_dim=img_dim, color=(100, 100, 200))
    layers.append(next_layer)
    next_layer.draw(next_shape)
    next_layer.show()
    # show result
    img = Layer.merge_and_draw(layers=layers, img=img)
    img.show()


def test_on_text_line():
    decoration_polygon: Polygon = Polygon(
        [(1625, 4526), (1625, 4530), (1632, 4548), (1636, 4595), (1641, 4603), (1649, 4604), (1652, 4602), (1653, 4599),
         (1652, 4585), (1654, 4568), (1653, 4551), (1650, 4539), (1645, 4524), (1639, 4519), (1636, 4518), (1630, 4519),
         (1625, 4526)])

    text_line_polygon: Polygon = Polygon(
        [(3866, 1238), (3868, 1247), (3879, 1256), (3924, 1260), (3931, 1259), (3935, 1256), (3960, 1254), (3964, 1257),
         (3968, 1257), (3999, 1249), (4009, 1249), (4014, 1246), (4027, 1233), (4030, 1232), (4044, 1252), (4046, 1257),
         (4049, 1259), (4096, 1253), (4113, 1258), (4135, 1273), (4146, 1276), (4154, 1276), (4163, 1271), (4176, 1254),
         (4205, 1255), (4238, 1252), (4257, 1240), (4275, 1224), (4293, 1242), (4293, 1252), (4299, 1258), (4350, 1255),
         (4383, 1239), (4411, 1247), (4411, 1256), (4409, 1261), (4409, 1296), (4411, 1308), (4416, 1313), (4422, 1312),
         (4425, 1308), (4424, 1289), (4426, 1275), (4427, 1270), (4433, 1260), (4502, 1270), (4534, 1266), (4556, 1266),
         (4575, 1271), (4654, 1269), (4682, 1274), (4710, 1275), (4720, 1271), (4745, 1244), (4742, 1236), (4736, 1232),
         (4711, 1227), (4687, 1227), (4673, 1213), (4667, 1204), (4659, 1200), (4648, 1202), (4642, 1207), (4612, 1215),
         (4603, 1224), (4530, 1223), (4441, 1228), (4417, 1220), (4409, 1216), (4378, 1220), (4329, 1203), (4320, 1198),
         (4293, 1197), (4270, 1210), (4246, 1186), (4217, 1179), (4195, 1178), (4169, 1185), (4126, 1215), (4045, 1213),
         (4039, 1214), (4021, 1222), (4014, 1223), (3987, 1212), (3981, 1212), (3975, 1215), (3959, 1219), (3938, 1215),
         (3884, 1217), (3875, 1219), (3870, 1224), (3866, 1238)])

    base_line: Line = Line([(3866, 1250), (4745, 1271)])

    centered_decoration_polygon, min_x1, min_y1 = center_polygon(decoration_polygon)
    centered_text_line_polygon, min_x2, min_y2 = center_polygon(text_line_polygon)
    centered_line, min_x3, min_y3 = center_polygon(base_line, min_x2, min_y2)
    centered_base_line: Line = Line(centered_line.xy)

    img_dim: ImageDimension = ImageDimension(centered_text_line_polygon.get_max_x(),
                                             centered_text_line_polygon.get_max_y())
    img = Image.new("RGB", size=img_dim.to_tuple())

    # create and decorate textline
    main_text_line = MainTextLine(centered_text_line_polygon, BaseLine(centered_base_line), color=(255, 100, 50))
    ascender_descender_text_line = AscenderDescenderRegion(text_line=main_text_line, x_height=42)

    # set visible and colors
    ascender_descender_text_line.descender_region.set_visible(True)
    ascender_descender_text_line.descender_region.set_color((255, 100, 0))
    ascender_descender_text_line.x_region.set_visible(True)
    ascender_descender_text_line.x_region.set_color((100, 255, 0))
    ascender_descender_text_line.ascender_region.set_visible(True)
    ascender_descender_text_line.ascender_region.set_color((0, 100, 255))
    ascender_descender_text_line.text_line.set_visible(True)
    ascender_descender_text_line.text_line.set_color((255, 255, 255))
    ascender_descender_text_line.base_line.set_visible(False)
    ascender_descender_text_line.base_line.set_color((255, 255, 255))

    layered_page_element: List[Layer] = ascender_descender_text_line.layer(img=img)
    layered_img = Layer.merge_and_draw(layered_page_element)
    layered_img.show()

def test_real_gt():
    start = time.time()

    original = Path("../../../../CB55/img/public-test/e-codices_fmb-cb-0055_0105r_max.jpg")
    pixel = Path("../../../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0105r_max.png")
    vector_gt = Path("../../../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0105r_max.xml")
    original_2 = Path("../../../../CB55/img/public-test/e-codices_fmb-cb-0055_0108v_max.jpg")
    pixel_2 = Path("../../../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0108v_max.png")
    vector_gt_2 = Path("../../../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0108v_max.xml")
    color_table = Path("../../../Resources/color_table.json")

    builder = BuilderV1(orig_img=original_2, px_gt_path=pixel_2, vector_gt_path=vector_gt_2, col_table=color_table,
                        vis_table=None)

    target_dim: ImageDimension = ImageDimension(4500, 6000)
    builder.crop(target_dim)

    target_dim: ImageDimension = ImageDimension(1800, 2400)

    # builder.resize(target_dim=target_dim)

    builder.decorate()

    color_table_instance = ColorTableReader().read(color_table)
    builder.color(color_table=color_table_instance)

    builder.set_visible()

    builder.construct()

    # page: Page = builder.get_GT()

    # page.px_gt.show()
    # page.raw_img.show()

    # builder.write(output_path = Path("../Resources/ResizedGT/"))
    #

    logging.info("program ended")
    end = time.time()
    logging.info("time passed: " + str(end - start))


def test_two_text_lines():
    img_dim: ImageDimension = ImageDimension(4872, 6496)
    img = Image.new("RGB", size=img_dim.to_tuple())
    # px_gt = PixelLevelGT(img_dim)

    decoration_polygon: Polygon = Polygon(
        [(1625, 4526), (1625, 4530), (1632, 4548), (1636, 4595), (1641, 4603), (1649, 4604), (1652, 4602), (1653, 4599),
         (1652, 4585), (1654, 4568), (1653, 4551), (1650, 4539), (1645, 4524), (1639, 4519), (1636, 4518), (1630, 4519),
         (1625, 4526)])

    text_line_polygon: Polygon = Polygon(
        [(3866, 1238), (3868, 1247), (3879, 1256), (3924, 1260), (3931, 1259), (3935, 1256), (3960, 1254), (3964, 1257),
         (3968, 1257), (3999, 1249), (4009, 1249), (4014, 1246), (4027, 1233), (4030, 1232), (4044, 1252), (4046, 1257),
         (4049, 1259), (4096, 1253), (4113, 1258), (4135, 1273), (4146, 1276), (4154, 1276), (4163, 1271), (4176, 1254),
         (4205, 1255), (4238, 1252), (4257, 1240), (4275, 1224), (4293, 1242), (4293, 1252), (4299, 1258), (4350, 1255),
         (4383, 1239), (4411, 1247), (4411, 1256), (4409, 1261), (4409, 1296), (4411, 1308), (4416, 1313), (4422, 1312),
         (4425, 1308), (4424, 1289), (4426, 1275), (4427, 1270), (4433, 1260), (4502, 1270), (4534, 1266), (4556, 1266),
         (4575, 1271), (4654, 1269), (4682, 1274), (4710, 1275), (4720, 1271), (4745, 1244), (4742, 1236), (4736, 1232),
         (4711, 1227), (4687, 1227), (4673, 1213), (4667, 1204), (4659, 1200), (4648, 1202), (4642, 1207), (4612, 1215),
         (4603, 1224), (4530, 1223), (4441, 1228), (4417, 1220), (4409, 1216), (4378, 1220), (4329, 1203), (4320, 1198),
         (4293, 1197), (4270, 1210), (4246, 1186), (4217, 1179), (4195, 1178), (4169, 1185), (4126, 1215), (4045, 1213),
         (4039, 1214), (4021, 1222), (4014, 1223), (3987, 1212), (3981, 1212), (3975, 1215), (3959, 1219), (3938, 1215),
         (3884, 1217), (3875, 1219), (3870, 1224), (3866, 1238)])

    base_line: BaseLine = BaseLine(Line([(3866, 1250), (4745, 1271)]))

    main_text_line = MainTextLine(polygon=text_line_polygon, base_line=base_line)
    main_text_line.set_visible(True)
    another_text_line = CommentTextLine(Polygon([(x, y + 500) for x, y in text_line_polygon.xy]),
                                        BaseLine(
                                            Line([(x, y + 500) for x, y in base_line.polygon.xy])))

    new_poly = Polygon([(x - 500, y + 200) for x, y in text_line_polygon.xy])
    ascender_descender_line = AscenderDescenderRegion(
        MainTextLine(new_poly, BaseLine(Line([(x - 500, y + 200) for x, y in base_line.polygon.xy]))), x_height=45)
    ascender_descender_line.set_visible(True)
    ascender_descender_line.x_region.set_color((255,0,0))
    ascender_descender_line.ascender_region.set_color((0, 255, 0))
    ascender_descender_line.descender_region.set_color((0, 255, 255))

    decoration = DecorationElement(decoration_polygon)
    decoration.set_visible(True)

    # create page layout
    main_text = MainText()
    main_text.add_elem(elem=main_text_line)
    main_text.add_elem(ascender_descender_line)

    comment_text = CommentText()
    comment_text.add_elem(another_text_line)

    decorations = Decorations()
    decorations.add_elem(decoration)

    # # test layer() in layout:
    # layered_maintext = main_text.layer(img=img)
    # layered_maintext.show()

    # creat text_region
    main_text_region = TextRegion(main_text)
    comment_text_region = TextRegion(comment_text)
    decoration_region = TextRegion(decorations)
    #
    # # test layer() of text_region
    # img_2 = Image.new("RGB", size=img_dim.to_tuple())
    # layered_maintext_region = main_text_region.layer(img_2)
    # layered_maintext_region.show()

    regions = []
    regions.append(main_text_region)
    regions.append(comment_text_region)
    regions.append(decoration_region)


    # test layer() of vector_gt
    img_2 = Image.new("RGB", size=img_dim.to_tuple())
    vector_gt = VectorGT(regions, img_dim=img_dim)
    layered_vector_gt = vector_gt.layer(img_2)
    layered_vector_gt.show()


if __name__ == '__main__':
    # test basic merge and draw()
    # test_merge_and_draw()

    # # test on a real text line
    # test_on_text_line()

    # Test two textlines
    #test_two_text_lines()

    # # test on real ground_truth
    test_real_gt()
