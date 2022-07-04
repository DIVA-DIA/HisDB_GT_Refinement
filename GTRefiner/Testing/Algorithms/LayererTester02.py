# Test if a built-in method layer() in PageElements does the job.

from typing import List

from HisDB_GT_Refinement.GTRefiner.Algorithms.Visitors.LazyLayerer import Layerer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation import PageLayout
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import BaseLine, MainTextLine, \
    DecorationElement, CommentTextLine, AscenderDescenderRegion
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import MainText, Decorations, \
    CommentText, TextRegion
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Polygon, Line

if __name__ == '__main__':
    img_dim: ImageDimension = ImageDimension(4872, 6496)
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
    another_text_line = CommentTextLine(Polygon([(x, y + 500) for x, y in text_line_polygon.xy]),
                                        BaseLine(
                                            Line([(x, y + 500) for x, y in base_line.polygon.xy])))

    new_poly = Polygon([(x - 500, y + 200) for x, y in text_line_polygon.xy])
    ascender_descender_line = AscenderDescenderRegion(
        MainTextLine(new_poly, BaseLine(Line([(x - 500, y + 200) for x, y in base_line.polygon.xy]))), x_height=45)

    decoration = DecorationElement(decoration_polygon)

    main_text_line.set_is_filled(True)
    another_text_line.set_is_filled(True)
    decoration.set_is_filled(True)
    ascender_descender_line.set_is_filled(True)

    # create page layout
    main_text = MainText()
    main_text.add_elem(elem=main_text_line)
    main_text.add_elem(ascender_descender_line)

    comment_text = CommentText()
    comment_text.add_elem(another_text_line)

    decorations = Decorations()
    decorations.add_elem(decoration)

    main_text_region = TextRegion(main_text)
    comment_text_region = TextRegion(comment_text)
    decoration_region = TextRegion(decorations)

    # create vector_gt
    vector_gt_list: List[TextRegion] = [main_text_region, comment_text_region, decoration_region]
    vector_gt = VectorGT(regions=vector_gt_list, img_dim=img_dim)

    # create Layerer
    lazy_layerer = Layerer(vector_gt)

    # visit the page_layout
    vector_gt.accept(lazy_layerer)

    # illustrate the new px_gt
    lazy_layerer.px_gt.show()
