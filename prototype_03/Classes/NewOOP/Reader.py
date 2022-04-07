# opens xml
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from typing import Tuple

from HisDB_GT_Refinement.prototype_03.Classes.NewOOP import Textline

from PIL import Image, ImageDraw

from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.Scalable import Scalable

# VectorBasedGT stores all information from the xmls. It also holds additional information, e.g. the
from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.VectorObject import Polygon, Line


class Reader(Scalable):

    def __init__(self, path: Path):
        self.textlines = self.get_text_line_from_xml(path) # should contain polygon & boundarybox
        self.baselines = self.get_baselines_from_xml(path) # should contain baseline (x,y) coordinates
        self.textregions = self.get_text_regions_xml(path) # should contain the regions


    def read_xml(self, xml_path: Path):
        patt = re.compile('\{.*\}')
        # load xml
        tree = ET.parse(str(xml_path))
        root = tree.getroot()
        ns = patt.match(
            root.tag).group()  # group returns the different submatches of the regex match (https://www.geeksforgeeks.org/re-matchobject-group-function-in-python-regex/)
        page_part = root[1]
        main_text = Textline.MainText()
        comments = Textline.CommentText()
        decorations = Textline.Decorations()
        text_regions = Textline.TextRegions()
        # parse out the polygons
        i = 0 # for debugger
        for text_region in page_part:
            for text_line in text_region.findall(ns + 'TextLine'):
                print(text_line.attrib)
                i = i + 1
                base_line_text = text_line.find(ns + 'Baseline').attrib['points']
                baseline = Line([tuple(map(int, pr.split(','))) for pr in base_line_text.split(' ')])
                polygon_text: str = text_line.find(ns + 'Coords').attrib['points']
                if text_line.attrib.get("id").startswith("textline"):
                    main_text.append_elem(Textline.MainTextLine(Polygon(polygon=self.str_to_polygon(polygon_text)), baseline=baseline))
                elif text_line.attrib.get("id").startswith("comment"):
                    comments.append_elem(Textline.CommentLine(Polygon(polygon=self.str_to_polygon(polygon_text)), baseline=baseline))
            # must be in outer loop due to file structure
            polygon_text: str = text_region.find(ns + 'Coords').attrib['points']
            if "TextRegion" in str(text_region.tag):
                color = (0,255,255)
                if text_region.attrib.get("id").startswith("region_textline"):
                    color = (255,255,255)
                text_regions.append_elem(
                    Textline.TextRegionElement(Polygon(polygon=self.str_to_polygon(polygon_text)), color))
            elif "GraphicRegion" in str(text_region.tag):
                decorations.append_elem(
                Textline.DecorationElement(Polygon(polygon=self.str_to_polygon(polygon_text))))
        return [main_text,comments,decorations,text_regions]


    def str_to_polygon(self, polygon_str : str):
        return [tuple(map(int, pr.split(','))) for pr in polygon_str.split(' ')]

    # TODO: each textline must be instantiated as TextLine: "Main-Text", "Comment" or "Decoration"
    def get_text_line_from_xml(self, xml_path: Path):
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


    # TODO: instantiate as BaseLine or add BaseLine to TextLine
    def get_baselines_from_xml(self, xml_path: Path):
        # fast der gleiche code wie get_polygons_from_xml(), ausser das Coords durch BaseLine ersetzt wurde.
        patt = re.compile('\{.*\}')
        # load xml
        tree = ET.parse(str(xml_path))
        root = tree.getroot()
        ns = patt.match(
            root.tag).group()  # group returns the different submatches of the regex match (https://www.geeksforgeeks.org/re-matchobject-group-function-in-python-regex/)
        page_part = root[1]
        baselines = []
        # parse out the polygons
        for text_region in page_part:
            for text_line in text_region.findall(ns + 'TextLine'):
                polygon_text = text_line.find(ns + 'Baseline').attrib['points']
                baselines.append([tuple(map(int, pr.split(','))) for pr in polygon_text.split(' ')])
        return baselines

    # TODO: Find out if text region should be in every TextLine
    def get_text_regions_xml(self, xml_path: Path):
        patt = re.compile('\{.*\}')
        # load xml
        tree = ET.parse(str(xml_path))
        root = tree.getroot()
        ns = patt.match(
            root.tag).group()  # group returns the different submatches of the regex match (https://www.geeksforgeeks.org/re-matchobject-group-function-in-python-regex/)
        page_part = root[1]
        bounding_boxes = []
        # parse out the polygons
        print("these are text_regions")
        for text_region in page_part:
                print(str(text_region.tag) + "-- tag")
                print(str(text_region.find("GraphicRegion")))
                polygon_text = text_region.find(ns + 'Coords').attrib['points']
                bounding_boxes.append([tuple(map(int, pr.split(','))) for pr in polygon_text.split(' ')])
        return bounding_boxes

    def show(self):
        img = Image.new("RGB", (4872, 6496))
        drawer = ImageDraw.Draw(img)
        for baseline in self.baselines:
            drawer.line(xy=baseline, fill=(255, 255, 255), width=2) # weiss

        for region in self.textregions:
            drawer.polygon(xy=region, outline=(255, 255, 0)) # gelb

        for textline in self.textlines:
            drawer.polygon(xy=textline, outline=(0, 255, 255)) # türkis
        img.show()

    def draw(self, drawer: ImageDraw):
        pass

    def resize(self, size: Tuple):
        print("Resize method nocht nicht implementiert (@ PAGE(Scalable)")


if __name__ == '__main__':
    path = Path("../../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0105r_max.xml")

    page = Reader(path)

    img = Image.new("RGB", (4872, 6496))
    drawer = ImageDraw.Draw(img)

    text = page.read_xml(path)
    for text_class in text:
        print(text_class.length())
        for elem in text_class.text_lines:
            elem.draw(drawer)
            print(elem.polygon.polygon)

    img.show()


    page.show()


