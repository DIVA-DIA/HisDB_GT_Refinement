from typing import Dict, List

from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import LayoutVisitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import GroundTruth
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import TextRegion, ImageDimension


class VectorGT(GroundTruth):

    def __init__(self, regions: List[TextRegion], img_dim: ImageDimension):
        super().__init__(img_dim)
        self.regions: List[TextRegion] = regions

    def accept(self, layout_visitor: LayoutVisitor):
        for region in self.regions:
            region.accept_layout_visitor(layout_visitor)

    def get_dim(self):
        return super().get_dim()

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        for layout in self.regions:
            for region in layout.text_regions:
                for elem in region.page_elements:
                    elem.resize(current_dim=current_dim,target_dim=target_dim)
        self.img_dim = target_dim

    def show(self):
        raise NotImplementedError

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        for layout in self.regions:
            for region in layout.text_regions:
                for elem in region.page_elements:
                    elem.crop(current_dim=current_dim, target_dim=target_dim, cut_left=cut_left)
        self.img_dim = target_dim


