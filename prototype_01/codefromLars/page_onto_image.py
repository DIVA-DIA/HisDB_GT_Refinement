import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
import re

from PIL import Image, ImageDraw


# draws the polygons onto the image
def overlay_img_with_xml(image_path: Path, xml_path: Path, output_path: Path):
    output_path.mkdir(exist_ok=True)
    polygons = get_polygons_from_xml(xml_path=xml_path)
    # colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255,255,255)]
    colors = [(240, 60, 60)]
    with Image.open(str(image_path)) as f:
        for i, polygon in enumerate(polygons):
            img = ImageDraw.Draw(f)
            color = colors[i % len(colors)]
            img.line(polygon, fill=color, width=1)
            #img.polygon(polygon, fill = color, outline = color)
        f.save(output_path / 'e-codices_fmb-cb-0055_0098v_max_outlined.png')


# get the polygons from the xml
def get_polygons_from_xml(xml_path: Path):
    patt = re.compile('\{.*\}')
    # load xml
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    ns = patt.match(root.tag).group() #group returns the different submatches of the regex match (https://www.geeksforgeeks.org/re-matchobject-group-function-in-python-regex/)
    page_part = root[1]
    polygons = []
    # parse out the polygons
    for text_region in page_part:
        for text_line in text_region.findall(ns + 'TextLine'):
            polygon_text = text_line.find(ns + 'Coords').attrib['points']
            polygons.append([tuple(map(int, pr.split(','))) for pr in polygon_text.split(' ')])

    return polygons


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-i', '--image_path', type=Path, required=True, help='Path to the image')
    # parser.add_argument('-x', '--xml_path', type=Path, required=True, help='Path to the page xml')
    # parser.add_argument('-o', '--output_path', type=Path, required=True, help='Path to the output folder')
    #
    # args = parser.parse_args()
    #
    # overlay_img_with_xml(**args.__dict__)

    original_png = Path("../../CB55/img/public-test/e-codices_fmb-cb-0055_0098v_max.jpg")
    xml_gt = Path("../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0098v_max.xml")
    pixel_level_gt = Path("../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0098v_max.png")
    white_background = Path("../Input/White_Background.png")
    all_different_colors = Path("../Input/with_all_different_colors_02.png")
    output = Path("../Output/polygons_outlined")


    # CB55 img public test with PAGE-gt
    # overlay_img_with_xml(original_png,xml_gt,output) # ever line a different color

    # CB55 pixel-level-gt
    overlay_img_with_xml(white_background, xml_gt, output)