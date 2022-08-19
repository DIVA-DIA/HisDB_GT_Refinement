from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import Visitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Scalable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT, RawImage
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT


class Resizer(Visitor):
    """Resize a page (and all it's ground-truth information, including the original image) to a target dimension.
    :param target_dim: Target dimension
    :type target_dim: ImageDimension
    """

    def __init__(self, target_dim: ImageDimension):
        """Constructor method"""
        self.target_dim = target_dim

    def visit_page(self, page: Page):
        """Resize a page (and all it's ground-truth information, including the original image) to a target dimension.
        :param target_dim: Target dimension
        :type target_dim: ImageDimension
        """
        current_dim = page.get_img_dim()
        page.vector_gt.resize(current_dim=current_dim, target_dim=self.target_dim)
        page.px_gt.resize(current_dim=current_dim,target_dim=self.target_dim)
        page.raw_img.resize(current_dim=current_dim,target_dim=self.target_dim)
