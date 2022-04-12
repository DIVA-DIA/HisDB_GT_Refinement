import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
import re
import logging
import datetime
from typing import List, Tuple
from xml.dom import minidom

import numpy as np
from PIL import Image, ImageDraw

from HisDB_GT_Refinement.prototype_02.Classes import MyPolygon
from HisDB_GT_Refinement.prototype_02.Classes.ColorPalette import create_color_palette

# TODO: make colors a parameter
# draws the polygons onto the image
from HisDB_GT_Refinement.prototype_02.Classes.MyPolygon import Polygon


# TODO: This method is flawed because it isn't generic. instead of xml_path, polygons would be nice.
def overlay_img_with_xml(image: Image, polygons: List[List[Tuple]], output_path: Path):
    output_path.mkdir(exist_ok=True)
    #polygons = get_polygons_from_xml(xml_path=xml_path)
    colors = create_color_palette(len(polygons))
    for i, polygon in enumerate(polygons):
        drawn_image = ImageDraw.Draw(image)
        color = colors[i]
        drawn_image.line(polygon, fill=color, width=1)
        # img.polygon(polygon, fill = color, outline = color)
    return image


# TODO: Get the different classes (comment, decoration, main-text) if necessary.
# get the polygons from the xml
def get_polygons_from_xml(xml_path: Path):
    patt = re.compile('\{.*\}')
    # load xml
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    ns = patt.match(
        root.tag).group()  # group returns the different submatches of the regex match (https://www.geeksforgeeks.org/re-matchobject-group-function-in-python-regex/)
    page_part = root[1]
    polygons = []
    # parse out the polygons
    for text_region in page_part:
        for text_line in text_region.findall(ns + 'TextLine'):
            polygon_text = text_line.find(ns + 'Coords').attrib['points']
            polygons.append([tuple(map(int, pr.split(','))) for pr in polygon_text.split(' ')])
    return polygons


def rescale_all_polygons(polygons, resize_factor):
    resized_polygons = []
    for polygon in polygons:
        my_polygon = MyPolygon.Polygon(polygon)
        new_polygon = MyPolygon.resize_polygon(polygon=my_polygon, resize_factor=resize_factor)
        resized_polygons.append(new_polygon)
    return resized_polygons


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-i', '--image_path', type=Path, required=True, help='Path to the image')
    # parser.add_argument('-x', '--xml_path', type=Path, required=True, help='Path to the page xml')
    # parser.add_argument('-o', '--output_path', type=Path, required=True, help='Path to the output folder')
    #
    # args = parser.parse_args()
    #
    # overlay_img_with_xml(**args.__dict__)

    original_png = Path("../../../CB55/img/public-test/e-codices_fmb-cb-0055_0098v_max.jpg")
    xml_gt = Path("../../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0098v_max.xml")
    pixel_level_gt = Path("../../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0098v_max.png")
    all_different_colors = Path("../Input/with_all_different_colors_02.png")
    output = Path("../../Output/polygons_different_colors_26.2/")

    # CB55 img public test with PAGE-gt
    # overlay_img_with_xml(original_png,xml_gt,output) # ever line a different color

    # CB55 pixel-level-gt
    overlay_img_with_xml(pixel_level_gt, xml_gt, output)

    gif = Path(output / "e-codices_fmb-cb-0055_0098v_max_colored.gif")
    rgb = Image.open(gif).convert("RGB")
    # rgb.show(title="Original image (before conversion)")
    img_as_array = np.asarray(rgb)
    # convert the image to an index based image
    pil_image = Image.fromarray(img_as_array).convert('P', palette=Image.ADAPTIVE, colors=256)
    print(pil_image.palette.colors)
