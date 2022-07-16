# TODO: write or find function that saves polygons as PAGE format
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List
from xml.dom import minidom
import logging
import datetime
import time

# reference: https://github.com/DIVA-DIA/Text-Line-Segmentation-Method-for-Medieval-Manuscripts/blob/master/src/line_segmentation/utils/XMLhandler.py
from PIL.Image import Image

from HisDB_GT_Refinement.prototype_02.Classes.PageOntoImage import get_polygons_from_xml, rescale_all_polygons


def writePAGEfile(output_path, text_lines="", text_region_coords="not provided", baselines=None):
    # Create root element and add the attributes
    root = ET.Element("PcGts")
    root.set("xmls", "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:schemaLocation", "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15/pagecontent.xsd")

    # Add metadata
    metadata = ET.SubElement(root, "Metadata")
    ET.SubElement(metadata, "Creator").text = "Michele Alberti, Vinaychandran Pondenkandath"
    ET.SubElement(metadata, "Created").text = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    ET.SubElement(metadata, "LastChange").text = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    # Add page
    page = ET.SubElement(root, "Page")

    # Add TextRegion
    textRegion = ET.SubElement(page, "TextRegion")
    textRegion.set("id", "region_textline")
    textRegion.set("custom", "0")

    # Add Coords
    ET.SubElement(textRegion, "Coords", points=text_region_coords)

    # Add TextLine
    for i, line in enumerate(text_lines):
        textLine = ET.SubElement(textRegion, "TextLine", id="textline_{}".format(i), custom="0")
        ET.SubElement(textLine, "Coords", points=line)
        if baselines:
            ET.SubElement(textLine, "Baseline", points=baselines[i])
        else:
            ET.SubElement(textLine, "Baseline", points="not provided")
        textEquiv = ET.SubElement(textLine, "TextEquiv")
        ET.SubElement(textEquiv, "Unicode")

    # Add TextEquiv to textRegion
    textEquiv = ET.SubElement(textRegion, "TextEquiv")
    ET.SubElement(textEquiv, "Unicode")

    #print(prettify(root))

    # Save on file
    file = open(output_path, "w")
    file.write(prettify(root))
    file.close()

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

if __name__ == '__main__':

    start = time.time()
    print("Program running")

    # input
    public_test = Path("../../../CB55/img/public-test/")
    original_png = Path("../../../CB55/img/public-test/")
    xml_gt = Path("../../../CB55/PAGE-gt/public-test/")
    pixel_level_gt = Path("../../../CB55/pixel-level-gt/public-test/")

    # output
    intermediate_result = Path("../Output/GT_1/Resized_PX_Based_GT_With_All_Pixels_Outside_Polygon_Set_To_Background/")
    out_put_path = Path("../../Output/PAGE/first_try_03.xml")

    # get all xml paths
    path_to_xml_gt: List[str] = sorted(os.listdir(xml_gt))

    # open xml and extract the polygons in PAGEs
    xml = Path(xml_gt / path_to_xml_gt[0])
    polygons = get_polygons_from_xml(xml)

    # resize polygons
    resized_polygons = rescale_all_polygons(polygons=polygons, resize_factor=4)

    writePAGEfile(output_path=out_put_path,text_lines=resized_polygons)
    end = time.time()
    print("Programm ended in {} seconds".format((end - start)))

