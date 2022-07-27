# opens xml
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from typing import Tuple, Dict

from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.GT_Buildingblocks import PageLayout

from PIL import Image, ImageDraw

from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.GT_Buildingblocks.ImageDimension import ImageDimension
from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.Interfaces.Scalable import Scalable

# VectorBasedGT stores all information from the xmls. It also holds additional information, e.g. the
from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.GT_Buildingblocks.VectorObject import Polygon, Line
from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.GT_Buildingblocks.layout_classes import LayoutClasses

class VectorGT(Scalable):

    def __init__(self, path: Path):
        self.img_dimension: ImageDimension = None
        self.text_elements: Dict[LayoutClasses, PageLayout.Layout] = self._read_xml(path)

    def get_main_text_lines(self) -> PageLayout.MainText:
        return self.text_elements.get(LayoutClasses.MAINTEXT)

    def get_comments(self) -> PageLayout.CommentText:
        return self.text_elements.get(LayoutClasses.COMMENT)

    def get_decorations(self) -> PageLayout.Decorations:
        return self.text_elements.get(LayoutClasses.DECORATION)

    def get_text_regions(self) -> PageLayout.TextRegions:
        return self.text_elements.get(LayoutClasses.TEXT_REGIONS)

    def _read_xml(self, xml_path: Path):
        patt = re.compile('\{.*\}')
        # load xml
        tree = ET.parse(str(xml_path))
        root = tree.getroot()
        ns = patt.match(
            root.tag).group()  # group returns the different submatches of the regex match (https://www.geeksforgeeks.org/re-matchobject-group-function-in-python-regex/)
        page_part = root[1]
        # initialize all the text Regions
        main_text = PageLayout.MainText()
        comments = PageLayout.CommentText()
        decorations = PageLayout.Decorations()
        text_regions = PageLayout.TextRegions()
        # initialize dictionary
        text_elements: Dict = {}
        # parse out the polygons
        i = 0  # for debugger
        if "Page" in str(page_part.tag):
            img_dimension = ImageDimension(width=int(page_part.attrib["imageWidth"]),
                                           height=int(page_part.attrib["imageHeight"]))
            self.img_dimension = img_dimension
        else:
            raise AttributeError("Didn't find any attribute: 'Page' and couldn't instantiate the ImageDimension")
        for text_region in page_part:
            for text_line in text_region.findall(ns + 'TextLine'):
                print(text_line.attrib)
                i = i + 1
                base_line_text = text_line.find(ns + 'Baseline').attrib['points']
                baseline = Line([tuple(map(int, pr.split(','))) for pr in base_line_text.split(' ')])
                polygon_text: str = text_line.find(ns + 'Coords').attrib['points']
                if text_line.attrib.get("id").startswith("textline"):
                    main_text.append_elem(
                        PageLayout.MainTextLine(Polygon(polygon=self._str_to_polygon(polygon_text)), baseline=baseline))
                elif text_line.attrib.get("id").startswith("comment"):
                    comments.append_elem(
                        PageLayout.CommentLine(Polygon(polygon=self._str_to_polygon(polygon_text)), baseline=baseline))
            # must be in outer loop due to file structure
            polygon_text: str = text_region.find(ns + 'Coords').attrib['points']
            if "TextRegion" in str(text_region.tag):
                color = (0, 255, 255)
                if text_region.attrib.get("id").startswith("region_textline"):
                    color = (255, 255, 255)
                text_regions.append_elem(
                    PageLayout.TextRegionElement(Polygon(polygon=self._str_to_polygon(polygon_text)), color))
            elif "GraphicRegion" in str(text_region.tag):
                decorations.append_elem(
                    PageLayout.DecorationElement(Polygon(polygon=self._str_to_polygon(polygon_text))))
        return {LayoutClasses.MAINTEXT: main_text,
                LayoutClasses.COMMENT: comments,
                LayoutClasses.DECORATION: decorations,
                LayoutClasses.TEXT_REGIONS: text_regions}

    def _str_to_polygon(self, polygon_str: str):
        return [tuple(map(int, pr.split(','))) for pr in polygon_str.split(' ')]

    def get_dimension(self) -> ImageDimension:
        return self.img_dimension

    def draw(self, drawer: ImageDraw):
        for key in self.text_elements:
            for elem in self.text_elements[key]:
                elem.draw(drawer=drawer)


    def set_filled(self, fill: Tuple[float,float,float] = None):
        for main_text_line in self.get_main_text_lines():
            main_text_line.set_fill(fill)

        for comment in self.get_comments():
            comment.set_fill(fill)

    def resize(self, scale_factor: Tuple[float,float]):
        for key in self.text_elements:
            for elem in self.text_elements[key]:
                elem.visit_page(scale_factor=scale_factor)
        self.img_dimension = self.img_dimension.scale(scale_factor)


    def crop(self, target_dim: ImageDimension, cut_left: bool):
        for key in self.text_elements:
            for elem in self.text_elements[key]:
                elem.visit_page(source_dim=self.img_dimension, target_dim=target_dim, cut_left=cut_left)
        self.img_dimension = target_dim



    def show(self, img: Image):
        drawer = ImageDraw.Draw(img)
        self.draw(drawer)
        img.show()


if __name__ == '__main__':
    path = Path("../../../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0105r_max.xml")

    page = VectorGT(path)
    page.set_filled(fill=None)

    img = Image.new("RGB", page.img_dimension.to_tuple())
    drawer = ImageDraw.Draw(img)

    # text = VectorGTRepresentation(path)
    # for text_class in text.text_elements:
    #     print(text_class.length())
    #     for elem in text_class.text_lines:
    #         elem.draw(drawer)
    #         print(elem.polygon.xy)

    # TODO: adjust the x-height
    target_dim = ImageDimension(2000, 3000)
    scale_factor = page.img_dimension.scale_factor(target_dim)
    page.resize(scale_factor=scale_factor)

    #page.crop(target_dim=target_dim, cut_left=True)

    page.draw(drawer)
    img.show()
