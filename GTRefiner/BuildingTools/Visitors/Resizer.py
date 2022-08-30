from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import Visitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Scalable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT, RawImage
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT


class Resizer(Visitor):
    """Resize a page (and all it's ground-truth information, including the original image) to a target dimension.
    The default implementation scales the PixelGT in four steps. As in the last presented strategy, first all relevant
    text pixels are set as visible True and all others as invisible False. In the next step, the image is blurred using
    Gaussian methods - the ground truth image is now in grayscale. Finally, the blurred image is bicubically
    interpolated and binarized again (according to Otsu, Niblack or Sauvola). Blurring leads to a thickening of the text
    elements. The more blurring is applied, the more the text elements merge into each other.
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
