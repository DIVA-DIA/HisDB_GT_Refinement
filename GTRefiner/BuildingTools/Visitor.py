from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page


class Visitor:
    """Adds external behaviour to the page class.
    """

    @abstractmethod
    def visit_page(self, page: Page):
        """ Visit the page and apply the new behaviour of the concrete implementation of this Visitor :class:
        `Visitor`."""
        pass
