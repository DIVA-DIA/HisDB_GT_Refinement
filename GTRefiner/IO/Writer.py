import json
from abc import abstractmethod
from pathlib import Path

from PIL.Image import Image

from GTRefiner.GTRepresentation import GroundTruth
from GTRefiner.GTRepresentation.PixelGTRepresentation.PixelGT import MyImage, PixelLevelGT, RawImage
from GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT


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
        """ Write the vector based ground truth with the build()-method provided by the vector ground truth.
        :param ground_truth: vector ground truth to be dumped to json
        :type ground_truth: VectorGT
        :param path: Output path
        :type path: Path
        """
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
        """ Write px-based ground truth image.
        :param ground_truth: pixel based ground truth image to be stored
        :type ground_truth: Image
        :param path: Output path
        :type path: Path
        """
        ground_truth.save(path)


class RawImageWriter(ImageWriter):
    @classmethod
    def write(cls, ground_truth: RawImage, path: Path, format: str = ".gif"):
        """ Write raw image (original image that may haven been resized and/or cropped).
        :param ground_truth: raw image to be stored, defaults to GIF.
        :type ground_truth: Image
        :param path: Output path
        :type path: Path
        """
        path = Path(str(path) + format)
        ground_truth.img.save(fp=path)

class GIFWriter(ImageWriter):

    @classmethod
    def write(cls, ground_truth: Image, path: Path):
        """ Store an image as GIF.
        :param ground_truth: raw image to be stored
        :type ground_truth: Image
        :param path: Output path
        :type path: Path
        """
        Image.save(ground_truth, fp=str(path) + ".gif")

class PNGWriter(ImageWriter):

    @classmethod
    def write(cls, ground_truth: Image, path: Path):
        """ Store an image as GIF.
        :param ground_truth: raw image to be stored
        :type ground_truth: Image
        :param path: Output path
        :type path: Path
        """
        Image.save(ground_truth, fp=str(path) + ".png")

