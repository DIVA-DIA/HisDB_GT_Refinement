from pathlib import Path

from HisDB_GT_Refinement.GTRefiner.Builder.Builder import GTBuilder
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Cropper import Cropper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Grouper import Grouper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Resizer import Resizer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Colorer import Colorer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Combiner import Combiner
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.TextLineDecorator import TextLineDecorator
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.VisibilityVisitor import VisibilityVisitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT, RawImage
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import ColorTable, VisibilityTable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT
from HisDB_GT_Refinement.GTRefiner.IO.Reader import XMLReader, PxGTReader, ImageReader, VisibilityTableReader, \
    ColorTableReader

# TODO: Execute() in Director and make everything accept "Page".
from HisDB_GT_Refinement.GTRefiner.IO.Writer import JSONWriter, GIFWriter


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
        cropper.visit_page(page=self.page)
        # self.page.px_gt.show()

    def resize(self, resizer: Resizer):
        super().resize(resizer)
        resizer.visit_page(page=self.page)
        # self.page.px_gt.show()

    def decorate(self, decorator: TextLineDecorator):
        super().decorate(decorator)
        decorator.visit_page(self.page)

    def group(self, grouper: Grouper):
        super().group(grouper)
        grouper.visit_page(self.page)

    def set_visible(self, visibilitor: VisibilityVisitor = VisibilityVisitor()):
        super().set_visible()
        visibilitor.visit_page(page=self.page)

    def set_color(self, colorer: Colorer = Colorer()):
        super().set_color()
        colorer.visit_page(page=self.page)

    def combine(self, combiner: Combiner):
        super().combine(combiner)
        combiner.visit_page(self.page)

    def write(self, output_path):
        super().write(output_path)
        JSONWriter.write(ground_truth=self.page.vector_gt, path=output_path)
        GIFWriter.write(ground_truth=self.page.px_gt.img, path=output_path)

    def get_GT(self) -> Page:
        return self.page
