from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import PixelLevelGT
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation import VectorGT


class Combiner:
    """ Combines as a vector ground truth :class: `VectorGT` with a pixel ground truth :class: PixelLevelGT.
    They must have the same dimension.
    """

    def combine(self, vector_gt: VectorGT, px_gt: PixelLevelGT):
        pass