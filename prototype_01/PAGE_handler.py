# This class is inspired by Lars' page onto_image script
# It stores the polygones from the PAGE-documents (xml) in lists
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from PIL import ImageDraw, Image

polygons = []

# TODO: It would be nice to not only parse the polygons, but to have the classes they belong to as well.
def get_polygons_from_xml(xml_path: Path):
    patt = re.compile('\{.*\}')
    # load xml
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    ns = patt.match(
        root.tag).group()  # group returns the different submatches of the regex match (https://www.geeksforgeeks.org/re-matchobject-group-function-in-python-regex/)
    page_part = root[1]
    # parse out the polygons
    for text_region in page_part:
        for text_line in text_region.findall(ns + 'TextLine'):
            polygon_text = text_line.find(ns + 'Coords').attrib['points']
            polygons.append([tuple(map(int, pr.split(','))) for pr in polygon_text.split(' ')])


def draw_polygons(output_path: Path):
    image = Image.new("RGB", (5000, 5000), (255, 255, 255))
    drawing = ImageDraw.Draw(image)
    for polygon in polygons:
        drawing.line(polygon, (150, 22, 56), width=5)
    image.save(output_path, "PNG")
    image.show()


if __name__ == '__main__':
    PAGE_xml = Path("../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0098v_max.xml")
    output_path = Path("Output/First_color_manipulations/drawn_polygons.png")
    get_polygons_from_xml(PAGE_xml)
    draw_polygons(output_path)
