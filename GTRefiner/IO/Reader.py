from abc import abstractmethod
from pathlib import Path
from typing import Any

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import GroundTruth, PixelLevelGT, VectorGT, MyImage, RawImage
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import VisibilityTable, ColorTable


class AbstractReader():

    @abstractmethod
    def read(self, path: Path) -> Any:
        pass


class GTReader(AbstractReader):

    @abstractmethod
    def read(self, path: Path) -> GroundTruth:
        pass


class XMLReader(GTReader):

    def read(self, path: Path) -> VectorGT:
        pass


class PxGTReader(GTReader):

    def read(self, path: Path) -> PixelLevelGT:
        pass


class ImageReader(GTReader):
    def read(self, path: Path) -> RawImage:
        pass


class TableReader(AbstractReader):

    @abstractmethod
    def read(self, path: Path) -> Any:
        pass


class VisibilityTableReader(TableReader):
    def read(self, path: Path) -> VisibilityTable:
        pass


class ColorTableReader(TableReader):
    def read(self, path: Path) -> ColorTable:
        pass
