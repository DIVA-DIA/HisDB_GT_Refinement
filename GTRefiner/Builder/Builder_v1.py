from pathlib import Path

from PIL import Image

from HisDB_GT_Refinement.GTRefiner.Builder.Builder import GTBuilder
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Combiner import Combiner
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Cropper import Cropper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Grouper import Grouper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Resizer import Resizer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.LazyLayerer import Layerer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.TextLineDecorator import TextLineDecorator, \
    AscenderDescenderDecorator
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT, RawImage
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import ColorTable, VisibilityTable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT
from HisDB_GT_Refinement.GTRefiner.IO.Reader import XMLReader, PxGTReader, ImageReader


class BuilderV1(GTBuilder):

    def __init__(self, vector_gt_path: Path, px_gt_path: Path, orig_img: Path):
        self.page = self.read(vector_gt_path=vector_gt_path,px_gt_path=px_gt_path, orig_img=orig_img)

    def read(self, vector_gt_path: Path, px_gt_path: Path, orig_img: Path) -> Page:
        vector_gt: VectorGT = XMLReader.read(vector_gt_path)
        px_gt: PixelLevelGT = PxGTReader.read(px_gt_path)
        raw_img: RawImage = ImageReader.read(orig_img)
        return Page(vector_gt=vector_gt, px_gt=px_gt, raw_img=raw_img)

    def crop(self, target_dim: ImageDimension, cut_left: bool = None, current_dim: ImageDimension = None):
        # TODO: Lars fragen. Ich habe oft Methoden von Interfaces die für jede Klasse etwas anders aussehen. Hier z.B. crop()-Methode,
        #  welche gar keine current_dim braucht.
        Cropper.crop(target_dim=target_dim, page=self.page)

    def resize(self, target_dim: ImageDimension, current_dim: ImageDimension=None):
        Resizer.resize(page=self.page, target_dim=target_dim)

    def decorate(self, decorator: TextLineDecorator=None):
        AscenderDescenderDecorator.decorate(self.page.vector_gt, 22)

    def group(self, grouper: Grouper):
        pass

    def set_visible(self, vis_table: VisibilityTable = None):
        for layout_cl in self.page.vector_gt.regions:
            for region in layout_cl.text_regions:
                for elem in region.page_elements:
                    elem.set_is_filled(True)

    def color(self, colorer: ColorTable, vector_gt: VectorGT):
        pass

    def layer(self):
        layerer = Layerer(self.page.vector_gt)
        for layout_cl in self.page.vector_gt.regions:
            layout_cl.accept_layout_visitor(layerer)
        self.page.px_gt = layerer.px_gt

    def combine_px_gts(self, comb: Combiner) -> Layer:
        pass

    def mask(self, Image, Layer) -> Image:
        pass

    def write(self, output_path):
        pass

    def get_GT(self) -> Page:
        return self.page