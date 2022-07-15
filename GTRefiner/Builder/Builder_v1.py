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
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT, RawImage
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import ColorTable, VisibilityTable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT
from HisDB_GT_Refinement.GTRefiner.IO.Reader import XMLReader, PxGTReader, ImageReader, VisibilityTableReader, \
    ColorTableReader

# TODO: Execute() in Director and make everything accept "Page".
from HisDB_GT_Refinement.GTRefiner.IO.Writer import JSONWriter, ImageWriter, RawImageWriter


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

    def crop(self, target_dim: ImageDimension, cut_left: bool = None, current_dim: ImageDimension = None):
        super().crop(current_dim, target_dim, cut_left)
        Cropper.crop(target_dim=target_dim, page=self.page)
        # self.page.px_gt.show()

    def resize(self, target_dim: ImageDimension, current_dim: ImageDimension = None):
        super().resize(current_dim, target_dim)
        Resizer.resize(page=self.page, target_dim=target_dim)
        # self.page.px_gt.show()

    def decorate(self, decorator: TextLineDecorator = None):
        super().decorate(decorator)
        AscenderDescenderDecorator.decorate(self.page.vector_gt, 42)

    def group(self, grouper: Grouper):
        super().group(grouper)
        pass

    def set_visible(self, vis_table: VisibilityTable = None):
        super().set_visible(vis_table)
        for layout_cl in self.page.vector_gt.regions:
            for region in layout_cl.text_regions:
                for i, elem in enumerate(region.page_elements):
                    elem.set_visible(True)
                    # debugging
                    # if elem.layout_class is LayoutClasses.DECORATION:
                    #     elem.set_visible(True)
                    # elif i%100 == 0:
                    #     # for better performance only show a few lines
                    #     elem.set_visible(True)
                    # else:
                    #     elem.set_visible(False)
        # for k, v in self.page.px_gt.levels.items():
        #     # if (k is LayoutClasses.COMMENT) or (k is Layout Classes.MAINTEXT) or (
        #     #         k is LayoutClasses.DECORATION):
        #     #     v.visible = False
        #     # else:
        #     v.visible = True

    def color(self, color_table: ColorTable):
        super().color(color_table)
        colors = color_table.table
        for k, color in colors.items():
            self.page.px_gt[k]._color = color
        for region in self.page.vector_gt.regions:
            for layout in region.text_regions:
                for elem in layout.page_elements:
                    elem.set_color(color_table=color_table)

    def layer(self) -> PixelLevelGT:
        super().layer()
        layerer = Layerer(self.page.vector_gt,px_gt=self.page.px_gt)


    # def combine_px_gts(self, comb: Combiner):
    #     super().combine_px_gts(comb)
    #     img = comb.combine(orig_px=self.page.px_gt, new_px_gt=self.layer())
    #     self.page.px_gt.img = img
    #     img.show()

    def write(self, output_path):
        super().write(output_path)
        JSONWriter.write(ground_truth=self.page.vector_gt, path=output_path)
        RawImageWriter.write(ground_truth=self.page.raw_img, path=output_path)

    def get_GT(self) -> Page:
        return self.page
