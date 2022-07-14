import json
from abc import abstractmethod
from pathlib import Path

from PIL.Image import Image

from HisDB_GT_Refinement.GTRefiner.GTRepresentation import GroundTruth
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import MyImage, PixelLevelGT, RawImage
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation import VectorGT


class AbstractWriter():
    @classmethod
    @abstractmethod
    def write(cls, ground_truth: GroundTruth, path: Path):
        pass


class VectorGTWriter(AbstractWriter):
    @classmethod
    @abstractmethod
    def write(cls, ground_truth: VectorGT, path: Path):
        pass


class XMLWriter(VectorGTWriter):
    @classmethod
    def write(cls, ground_truth: VectorGT, path: Path):
        pass


class JSONWriter(VectorGTWriter):

    @classmethod
    def write(cls, ground_truth: VectorGT, path: Path):
        path = Path(str(path) + ".json")
        dict = ground_truth.build()
        json.dump(dict, open(path, "w"))


class ImageWriter(AbstractWriter):

    @classmethod
    @abstractmethod
    def write(cls, ground_truth: MyImage, path: Path):
        # path = Path(str(path) + "v1.gif")
        # ground_truth.img.save(path)
        pass


class PXGTWriter(ImageWriter):
    @classmethod
    def write(cls, ground_truth: Image, path: Path):
        ground_truth.save(path)


class RawImageWriter(ImageWriter):
    @classmethod
    def write(cls, ground_truth: RawImage, path: Path):
        path = Path(str(path) + ".gif")
        ground_truth.img.save(fp=path)
