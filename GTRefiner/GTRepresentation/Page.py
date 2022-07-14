from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import *
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT, RawImage
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import VisibilityTable, ColorTable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT


class Page(Scalable, Croppable, Showable):

    def __init__(self, vector_gt: VectorGT, px_gt: PixelLevelGT, raw_img: RawImage,vis_table: VisibilityTable, col_table: ColorTable):
        self.vector_gt: VectorGT = vector_gt
        self.px_gt: PixelLevelGT = px_gt
        self.raw_img: RawImage = raw_img
        self.vis_table: VisibilityTable = vis_table
        self.col_table: ColorTable = col_table
        self.img_dim = vector_gt.img_dim
        assert self.vector_gt.img_dim == self.px_gt.img_dim
        assert self.px_gt.img_dim == self.raw_img.img_dim