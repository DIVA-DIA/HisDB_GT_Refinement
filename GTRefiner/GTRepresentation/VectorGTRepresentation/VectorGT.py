from typing import Dict, List
import numpy as np

from PIL import ImageDraw, ImageChops
from PIL import Image

from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import LayoutVisitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import GroundTruth
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Dictionable, Scalable, Croppable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import TextRegion, ImageDimension


class VectorGT(GroundTruth, Dictionable, Scalable, Croppable):

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
        img = Image.new("RGB", size=self.img_dim.to_tuple())
        drawer = ImageDraw.Draw(img)
        for layout in self.regions:
            for region in layout.text_regions:
                for elem in region.page_elements:
                    elem.draw(drawer=drawer)
        img.show()

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        for layout in self.regions:
            for region in layout.text_regions:
                for elem in region.page_elements:
                    elem.crop(current_dim=current_dim, target_dim=target_dim, cut_left=cut_left)
        self.img_dim = target_dim

    def build(self) -> Dict:
        global_dict = {"ImageDimension":self.img_dim.to_tuple()}
        dict = {}
        for i, region in enumerate(self.regions):
            region_dict = {}
            region_dict.update(region.build())
            dict[type(region).__name__ + " " + str(i)] = region_dict
        global_dict["Vector Ground Truth"] = dict
        return global_dict

    def __eq__(self, other):
        if not type(other) is type(self):
            return False
        img_1 = Image.new("RGB", size=self.img_dim.to_tuple())
        drawer_1 = ImageDraw.Draw(img_1)
        for layout in self.regions:
            for region in layout.text_regions:
                for elem in region.page_elements:
                    elem.draw(drawer=drawer_1)
        img_as_array_1 = np.asarray(img_1)

        img_2 = Image.new("RGB", size=other.img_dim.to_tuple())
        drawer_2 = ImageDraw.Draw(img_2)
        for layout in other.regions:
            for region in layout.text_regions:
                for elem in region.page_elements:
                    elem.draw(drawer=drawer_2)
        img_as_array_2 = np.asarray(img_2)
        # for debugging
        # what_is_missing = np.logical_xor(img_as_array_1,img_as_array_2)
        # what_is_missing = np.where(what_is_missing,255,0)
        # img = Image.fromarray(what_is_missing.astype("uint8"))
        # img.show()
        return (img_as_array_1==img_as_array_2).all()



