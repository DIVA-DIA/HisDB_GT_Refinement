from GTRefiner.GTRepresentation.Interfaces.GTInterfaces import *
from GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT, RawImage
from GTRefiner.GTRepresentation.Table import VisibilityTable, ColorTable
from GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT


class Page(Scalable, Croppable, Showable):
    """ Stores all ground truth information of an image (including the original image, the vector gt and the pixel-based
    ground truth) and provides basic functionality for its manipulation such as scalability, croppability and
    showability.
    :param vector_gt: Stores polyogons of the various text elements (maintextline, decoration, textregion, etc.)
    :type vector_gt: VectorGT
    :param px_gt: Stores the original pixel level ground truth and its different information levels as :class: `Layers`.
    :type px_gt: PixelLevelGT
    :param raw_img: Stores the original image.
    :type raw_img: RawImage
    :param vis_table: Defines the visibility for the ground truth objects (texelements of the vector gt, levels of the
    pixel gt)
    :type vis_table: VisibilityTable
    :param col_table: Defines the colors for the ground truth objects (texelements of the vector gt, levels of the
    pixel gt)
    :type col_table: ColorTable
    """

    def __init__(self, vector_gt: VectorGT, px_gt: PixelLevelGT, raw_img: RawImage, vis_table: VisibilityTable,
                 col_table: ColorTable):
        self.vector_gt: VectorGT = vector_gt
        self.px_gt: PixelLevelGT = px_gt
        self.raw_img: RawImage = raw_img
        self.vis_table: VisibilityTable = vis_table
        self.col_table: ColorTable = col_table
        assert self.vector_gt.img_dim == self.px_gt.img_dim
        assert self.px_gt.img_dim == self.raw_img.img_dim

    def get_img_dim(self):
        """ Get the ground truth's dimension.
        :return: dimension of the ground truth.
        :rtype: ImageDimension
        """
        assert self.vector_gt.img_dim == self.px_gt.img_dim
        return self.vector_gt.img_dim

    def visit_page(self, visitor):
        """ Accepts visitors to manipulate the page and add further functionalities.
        :param visitor: manipulates the page (or invokes it's methods) to add specific behaviour
        :type visitor: Visitor
        """
        visitor.visit_page(self)
