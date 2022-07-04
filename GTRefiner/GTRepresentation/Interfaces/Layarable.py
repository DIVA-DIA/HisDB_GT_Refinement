from abc import abstractmethod


# Isolated from the other interfaces in order to avoid circular import.
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT


class Layarable:

    @abstractmethod
    def layer(self, px_gt: PixelLevelGT):
        """ Translates the vector_gt information into pixel information and stores it on the corresponding
        :class: `LayoutClasses` layer."""
        pass