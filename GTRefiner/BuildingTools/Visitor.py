from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import PageElement
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import TextRegion, Layout
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT


class Visitor:

    @abstractmethod
    def visit_page(self, page: Page):
        pass

    # @abstractmethod
    # def visit_vector_gt(self, vector_gt: VectorGT):
    #     pass
    #
    # @abstractmethod
    # def visit_pixel_gt(self, pixel_gt: PixelLevelGT):
    #     pass
    #
    # @abstractmethod
    # def visit_text_region(self, region: TextRegion):
    #     pass
    #
    # @abstractmethod
    # def visit_layout(self, layout: Layout):
    #     pass
    #
    # @abstractmethod
    # def visit_page_layout(self, page_elem: PageElement):
    #     pass
    #
