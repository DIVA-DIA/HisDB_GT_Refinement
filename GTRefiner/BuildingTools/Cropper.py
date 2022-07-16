from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Croppable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT, RawImage
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT


class Cropper:

    def __init__(self, target_dim: ImageDimension):
        self.target_dim = target_dim

    def crop(self, page:Page):
        current_dim = page.get_img_dim()
        cut_left = page.raw_img.get_cut_side()
        page.vector_gt.crop(current_dim=current_dim, target_dim=self.target_dim, cut_left=cut_left)
        page.px_gt.crop(current_dim=current_dim,target_dim=self.target_dim,cut_left=cut_left)
        page.raw_img.crop(current_dim=current_dim,target_dim=self.target_dim,cut_left=cut_left)