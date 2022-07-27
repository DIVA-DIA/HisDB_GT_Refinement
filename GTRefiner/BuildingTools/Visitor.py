from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page


class Visitor:

    @abstractmethod
    def visit_page(self, page: Page):
        pass