from pathlib import Path
from typing import List

from PIL import Image, ImageDraw

from GTRefiner.BuildingTools.Visitors.TextLineDecorator import AscenderDescenderDecorator
from GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT
from GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Polygon, Rectangle, \
    Line, Quadrilateral
from GTRefiner.IO.Reader import XMLReader, JSONReader
from GTRefiner.IO.Writer import JSONWriter

if __name__ == '__main__':
    # test vector_gt
    vector_gt_path = Path("../../../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0105r_max.xml")
    vector_gt_orig: VectorGT = XMLReader.read(path=vector_gt_path)

    AscenderDescenderDecorator().visit_page(vector_gt_orig, 42)

    out_put_fp = Path(
        "../../Resources/IO_JSON/version_with__name__in_build()_with_ascenders_descenders_with_textregion_names")

    JSONWriter().write(ground_truth=vector_gt_orig, path=out_put_fp)

    #vector_gt_orig.show()

    vector_gt_after_json_writing: VectorGT = JSONReader().read(Path(str(out_put_fp) + ".json"))
    vector_gt_after_json_writing.show()

    #AscenderDescenderDecorator().decorate(vector_gt_after_json_writing, 42)

    # Prove that their both the same after writing to a json and reading the json.
    assert vector_gt_orig == vector_gt_after_json_writing

