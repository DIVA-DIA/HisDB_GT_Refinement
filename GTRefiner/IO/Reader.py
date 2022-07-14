import json
import re
import xml.etree.ElementTree as ET
import numpy as np
from abc import abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Tuple

from PIL import Image

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import GroundTruth
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT, RawImage
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import VisibilityTable, ColorTable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation import PageLayout
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import BaseLine
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import TextRegion
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Line, Polygon


class AbstractReader():

    @classmethod
    @abstractmethod
    def read(cls, path: Path) -> Any:
        pass


class GTReader(AbstractReader):

    @classmethod
    @abstractmethod
    def read(cls, path: Path) -> GroundTruth:
        pass


class XMLReader(GTReader):

    @classmethod
    def read(cls, path: Path) -> VectorGT:
        return cls._read_xml(xml_path=path)

    @classmethod
    def _read_xml(cls, xml_path: Path):
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
        # initialize dictionary
        text_elements: Dict = {}
        # parse out the polygons
        i = 0  # for debugger
        if "Page" in str(page_part.tag):
            img_dimension = ImageDimension(width=int(page_part.attrib["imageWidth"]),
                                           height=int(page_part.attrib["imageHeight"]))
        else:
            raise AttributeError("Didn't find any attribute: 'Page' and couldn't instantiate the ImageDimension")
        for text_region in page_part:
            for text_line in text_region.findall(ns + 'TextLine'):
                i = i + 1
                base_line_text = text_line.find(ns + 'Baseline').attrib['points']
                baseline = BaseLine(Line([tuple(map(int, pr.split(','))) for pr in base_line_text.split(' ')]))
                polygon_text: str = text_line.find(ns + 'Coords').attrib['points']
                if text_line.attrib.get("id").startswith("textline"):
                    main_text.add_elem(
                        PageLayout.MainTextLine(Polygon(xy=cls._str_to_polygon(polygon_text)),
                                                base_line=baseline))
                elif text_line.attrib.get("id").startswith("comment"):
                    comments.add_elem(
                        PageLayout.CommentTextLine(Polygon(xy=cls._str_to_polygon(polygon_text)),
                                                   base_line=baseline))
            # # must be in outer loop due to file structure
            # polygon_text: str = text_region.find(ns + 'Coords').attrib['points']
            # if "TextRegion" in str(text_region.tag):
            #     color = (0, 255, 255)
            #     if text_region.attrib.get("id").startswith("region_textline"):
            #         color = (255, 255, 255)
            #     text_regions.append_elem(
            #         PageLayout.TextRegionElement(Polygon(polygon=self._str_to_polygon(polygon_text)), color))
            if "GraphicRegion" in str(text_region.tag):
                decorations.add_elem(
                    PageLayout.DecorationElement(Polygon(xy=cls._str_to_polygon(polygon_text))))
        return VectorGT([TextRegion(main_text), TextRegion(comments), TextRegion(decorations)], img_dim=img_dimension)

    @classmethod
    def _str_to_polygon(cls, polygon_str: str) -> List[Tuple]:
        return [tuple(map(int, pr.split(','))) for pr in polygon_str.split(' ')]


class PxGTReader(GTReader):

    @classmethod
    def read(cls, path: Path) -> PixelLevelGT:
        return cls._hisdb_to_bin_images(path)

    @classmethod
    def _hisdb_to_bin_images(cls, path: Path) -> PixelLevelGT:
        """
        Find out the different classes that are encoded in the image and convert them to binary images.
        :return: dict of binary images Dict[LayoutClasses, Layer]
        """
        img: Image = Image.open(path).convert("RGB")
        img_array = np.asarray(img)
        px_gt: PixelLevelGT = PixelLevelGT(img=img)

        # remove border pixels
        img_array_classes = img_array[:, :, 2]
        # 1: background, 2: comment, 4: decoration, 8: maintext
        # 6: comment + decoration, 12: maintext + decoration
        categories = np.unique(img_array_classes)[1:]

        for category in categories:
            # remove border pixels
            array_border = np.logical_not(img_array[:, :, 0] > 0)
            blue_chan = np.where(array_border, img_array_classes, 0)

            # set pixel which are equal to category to 255
            blue_chan = np.where(blue_chan[:, :] == category, 255, 0)

            px_gt.levels[LayoutClasses(category)] = Layer(blue_chan.astype(np.uint8))
        return px_gt


class ImageReader(GTReader):

    @classmethod
    def read(cls, path: Path) -> RawImage:
        img: Image = Image.open(path).convert("RGB")
        return RawImage(img)


class TableReader(AbstractReader):

    @classmethod
    @abstractmethod
    def read(cls, path: Path) -> Any:
        pass


class VisibilityTableReader(TableReader):

    @classmethod
    def read(cls, path: Path) -> VisibilityTable:
        # read json and convert to {LayoutClasses: Tuple}
        data = json.load(open(path))
        data = {LayoutClasses.str_to_enum(k): tuple(v) for (k, v) in data.items()}
        print(data)


class ColorTableReader(TableReader):
    @classmethod
    def read(cls, path: Path) -> ColorTable:
        data = json.load(open(path))
        data = {LayoutClasses.str_to_enum(k): tuple(v) for (k, v) in data.items()}
        return ColorTable(data)
