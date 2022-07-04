from pathlib import Path

from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.LazyLayerer import Layerer
from HisDB_GT_Refinement.GTRefiner.IO.Reader import XMLReader

if __name__ == '__main__':
    # read it
    page = Path("../../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0105r_max.xml")
    reader = XMLReader()
    vector_gt = reader.read(page)

    # activate all polygons it
    for region in vector_gt.regions:
        for layout in region.text_regions:
            for elem in layout.page_elements:
                elem.set_is_filled(True)

    # create Layerer
    layout_visitor = Layerer(vector_gt)

    # visit the page_layout
    vector_gt.accept(layout_visitor)

    # illustrate the new px_gt
    layout_visitor.px_gt.show()