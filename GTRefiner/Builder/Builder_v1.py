from pathlib import Path

from HisDB_GT_Refinement.GTRefiner.Builder.Builder import GTBuilder
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Cropper import Cropper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Grouper import Grouper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Resizer import Resizer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Colorer import Colorer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Combiner import Combiner
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.TextLineDecorator import TextLineDecorator
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT, RawImage
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import ColorTable, VisibilityTable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT
from HisDB_GT_Refinement.GTRefiner.IO.Reader import XMLReader, PxGTReader, ImageReader, VisibilityTableReader, \
    ColorTableReader

# TODO: Execute() in Director and make everything accept "Page".
from HisDB_GT_Refinement.GTRefiner.IO.Writer import JSONWriter, RawImageWriter, GIFWriter


class BuilderV1(GTBuilder):

    def __init__(self, vector_gt_path: Path, px_gt_path: Path, orig_img: Path, vis_table: Path, col_table: Path):
        self.page: Page = self.read(vector_gt_path=vector_gt_path, px_gt_path=px_gt_path, orig_img=orig_img,
                                    vis_table=vis_table, col_table=col_table)

    def read(self, vector_gt_path: Path, px_gt_path: Path, orig_img: Path, vis_table: Path, col_table: Path) -> Page:
        super().read(vector_gt_path, px_gt_path, orig_img, vis_table, col_table)
        vector_gt: VectorGT = XMLReader.read(vector_gt_path)
        px_gt: PixelLevelGT = PxGTReader.read(px_gt_path)
        raw_img: RawImage = ImageReader.read(orig_img)
        vis_table: VisibilityTable = VisibilityTableReader.read(vis_table)
        col_table: ColorTable = ColorTableReader.read(col_table)
        # px_gt.show()
        return Page(vector_gt=vector_gt, px_gt=px_gt, raw_img=raw_img, vis_table=vis_table, col_table=col_table)

    def crop(self, cropper: Cropper):
        super().crop(cropper)
        cropper.crop(page=self.page)
        # self.page.px_gt.show()

    def resize(self, resizer: Resizer):
        super().resize(resizer)
        resizer.resize(page=self.page)
        # self.page.px_gt.show()

    def decorate(self, decorator: TextLineDecorator):
        super().decorate(decorator)
        decorator.decorate(self.page)

    def group(self, grouper: Grouper):
        super().group(grouper)
        pass

    def set_visible(self):
        super().set_visible()
        for region in self.page.vector_gt.regions:
            for layout in region.text_regions:
                for elem in layout.page_elements:
                    elem.set_visible(vis_table=self.page.vis_table)
        self.page.px_gt.set_visible(vis_table=self.page.vis_table)

    def set_color(self):
        super().set_color()
        for region in self.page.vector_gt.regions:
            for layout in region.text_regions:
                for elem in layout.page_elements:
                    elem.set_color(color_table=self.page.col_table)
        self.page.px_gt.set_color(color_table=self.page.col_table)

    def construct(self, combiner: Combiner):
        super().construct(combiner)
        combiner.construct(self.page)

    def write(self, output_path):
        super().write(output_path)
        JSONWriter.write(ground_truth=self.page.vector_gt, path=output_path)
        GIFWriter.write(ground_truth=self.page.px_gt.img, path=output_path)

    def get_GT(self) -> Page:
        return self.page
