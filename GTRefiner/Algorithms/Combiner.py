from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import VectorGT, PixelLevelGT


class Combiner:
    """ Combines as a vector ground truth :class: `VectorGT` with a pixel ground truth :class: PixelLevelGT.
    They must have the same dimension.
    """

    def combine(self, vector_gt: VectorGT, px_gt: PixelLevelGT):
        pass