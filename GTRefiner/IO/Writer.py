from abc import abstractmethod
from pathlib import Path

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import GroundTruth, PixelLevelGT, VectorGT, MyImage, RawImage


class AbstractWriter():

    @abstractmethod
    def write(self, ground_truth: GroundTruth, path: Path):
        pass


class VectorGTWriter(AbstractWriter):

    @abstractmethod
    def write(self, ground_truth: VectorGT, path: Path):
        pass


class XMLWriter(VectorGTWriter):

    def write(self, ground_truth: VectorGT, path: Path):
        pass


class JSONWriter(VectorGTWriter):

    def write(self, ground_truth: VectorGT, path: Path):
        pass


class ImageWriter(AbstractWriter):

    @abstractmethod
    def write(self, ground_truth: MyImage, path: Path):
        pass


class PXGTWriter(ImageWriter):
    def write(self, ground_truth: PixelLevelGT, path: Path):
        pass


class ImageWriter(ImageWriter):
    def write(self, ground_truth: RawImage, path: Path):
        pass

