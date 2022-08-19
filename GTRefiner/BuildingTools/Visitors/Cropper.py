from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import Visitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page

class Cropper(Visitor):

    def __init__(self, target_dim: ImageDimension):
        """
        Crops all elements of page :class: `Page` to a given target dimension.
        :param target_dim: defines the target dimension.
        :type target_dim: ImageDimension
        """
        self.target_dim = target_dim

    def visit_page(self, page:Page):
        """Default implementation of Cropper
        :param page: Crops all elements of page :class: `Page` to a given target dimension, where a page can be cut
        left or cut right. This is figured out algorithmically.
        :type page: Page
        """
        current_dim = page.get_img_dim()
        cut_left = page.raw_img.get_cut_side()
        page.vector_gt.crop(current_dim=current_dim, target_dim=self.target_dim, cut_left=cut_left)
        page.px_gt.crop(current_dim=current_dim,target_dim=self.target_dim,cut_left=cut_left)
        page.raw_img.crop(current_dim=current_dim,target_dim=self.target_dim,cut_left=cut_left)