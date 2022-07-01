from typing import List
import unittest
import copy

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import *

if __name__ == '__main__':
    # vector_objects
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

    # create the different page elements
    page_elements: List[PageElement] = list()

    # Instantiating legal objects working fine?
    page_elements.append(DecorationElement(copy.deepcopy(decoration_polygon)))
    page_elements.append(MainTextLine(copy.deepcopy(text_line_polygon), copy.deepcopy(base_line)))
    page_elements.append(CommentTextLine(copy.deepcopy(text_line_polygon), copy.deepcopy(base_line)))
    page_elements.append(
        AscenderDescenderRegion(MainTextLine(copy.deepcopy(text_line_polygon), copy.deepcopy(base_line)), 45))

    # # Show all of the page elements and test the centered method.
    # for elem in page_elements:
    #     elem.show()

    img_dim: ImageDimension = ImageDimension(4872, 6496)

    # # Test the drawing method on black background
    # for elem in page_elements:
    #     img = Image.new("RGB", img_dim.to_tuple(), (0, 0, 0))
    #     drawer = ImageDraw.Draw(img)
    #     elem.draw(drawer=drawer)
    #     img.show()
    #
    # # Test the drawing method on black background and test is_filled
    # for elem in page_elements:
    #     elem.is_filled = True
    #     img = Image.new("RGB", img_dim.to_tuple(), (0, 0, 0))
    #     drawer = ImageDraw.Draw(img)
    #     elem.draw(drawer=drawer)
    #     img.show()
    #     elem.is_filled = False

    # # Test if it's possible to draw custom colors via set draw() method.
    # for elem in page_elements:
    #     elem.set_is_filled(True)
    #     img = Image.new("RGB", img_dim.to_tuple(), color=(0,0,0))
    #     drawer = ImageDraw.Draw(img)
    #     elem.draw(drawer=drawer,color=(120,80,250))
    #     img.show()
    #     elem.set_is_filled(False)
    #
    # # # Test if LayoutClasses can be used to custom color.
    # # TODO: Lars fragen, ob ich irgendwie diesen Warnungen irgendwie aus dem Weg gehen kann.
    # for elem in page_elements:
    #     if LayoutClasses.ASCENDER in elem.layout_class:
    #         elem.ascender_region.set_color((200, 0, 200))  # pink
    #         elem.ascender_region.set_is_filled(True)
    #     if LayoutClasses.DESCENDER in elem.layout_class:
    #         elem.descender_region.set_color((50, 0, 200))  # dark blue
    #         elem.descender_region.set_is_filled(True)
    #     if LayoutClasses.XREGION in elem.layout_class:
    #         elem.x_region.set_color((50, 100, 200))  # brighter blue
    #         elem.x_region.set_is_filled(True)
    #     img = Image.new("RGB", img_dim.to_tuple(), (0, 0, 0))
    #     drawer = ImageDraw.Draw(img)
    #     elem.draw(drawer=drawer)
    #     img.show()
    #     elem.is_filled = False

    # # Test if it's possible to draw on a binary picture via set set_is_filled()
    # for elem in page_elements:
    #     elem.set_is_filled(True)
    #     elem.set_color((1,))
    #     img = Image.new("1", img_dim.to_tuple(), color=(0,))
    #     drawer = ImageDraw.Draw(img)
    #     elem.draw(drawer=drawer)
    #     img.show()
    #     elem.set_color((255,255,255))
    #     elem.set_is_filled(False)

    # # Test if it's possible to draw on a binary picture via set draw() method.
    # for elem in page_elements:
    #     elem.set_is_filled(True)
    #     img = Image.new("1", img_dim.to_tuple(), color=(0,))
    #     drawer = ImageDraw.Draw(img)
    #     elem.draw(drawer=drawer,color=(1,))
    #     img.show()
    #     elem.set_is_filled(False)

    # # Test cropping & draw cropped version
    # #   create reference image
    # reference_img = Image.new("RGB", img_dim.to_tuple(), (0, 0, 0))
    # drawer = ImageDraw.Draw(reference_img)
    # page_elements[1].set_color((255, 0, 0))
    # page_elements[1].is_filled = True
    # page_elements[1].draw(drawer)
    # page_elements[1].set_color((255, 255, 255))
    # page_elements[1].is_filled = False
    # reference_img.show()
    # #   do the cropping
    # target_dim = ImageDimension(4500, 4500)
    # for elem in page_elements:
    #     elem.is_filled = True
    #     elem.crop(current_dim=img_dim, target_dim=target_dim, cut_left=True)
    #     img = Image.new("RGB", target_dim.to_tuple(), (10, 20, 30))
    #     drawer = ImageDraw.Draw(img)
    #     elem.draw(drawer=drawer)
    #     img.show()
    #     elem.is_filled = False
    #     assert img.size != reference_img.size
    #
    # cropped_polygon: Polygon = page_elements[1].polygon
    # assert cropped_polygon.xy != text_line_polygon.xy  # should be different after being cropped
    # assert cropped_polygon.xy == page_elements[
    #     2].polygon.xy  # should be equal to the other cropped polygons (else there would be a reference problem)
    # assert cropped_polygon.xy == page_elements[
    #     3].polygon.xy  # should be equal to the other cropped polygons (else there would be a reference problem)
    #
    # # Test resizing
    # #   create reference image
    # reference_img = Image.new("RGB", img_dim.to_tuple(), (0, 50, 20))
    # drawer = ImageDraw.Draw(reference_img)
    # #   do the resizing
    # target_dim = ImageDimension(1200, 1600)
    # for elem in page_elements:
    #     elem.resize(current_dim=img_dim, target_dim=target_dim)
    #     img = Image.new("RGB", target_dim.to_tuple(), (0, 50, 20))
    #     drawer = ImageDraw.Draw(img)
    #     elem.draw(drawer=drawer)
    #     img.show()
    # resized_polygon: Polygon = page_elements[1].polygon
    # assert resized_polygon.xy != text_line_polygon.xy  # should be different after being resized
    # assert resized_polygon.xy == page_elements[2].polygon.xy
    # assert resized_polygon.xy == page_elements[3].polygon.xy
