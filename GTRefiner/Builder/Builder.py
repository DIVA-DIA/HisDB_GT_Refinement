from pathlib import Path
from PIL import Image
from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.BuildingTools.Combiner import Combiner
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Grouper import Grouper
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Croppable, Scalable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.Layarable import Layarable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page, ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import VisibilityTable, ColorTable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import TextLineDecoration
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorGT import VectorGT


class GTBuilder(Croppable, Scalable, Layarable):

    @abstractmethod
    def read(self, vector_gt_path: Path, px_gt_path: Path, orig_img: Path):
        pass

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        pass

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        pass

    @abstractmethod
    def decorate(self, decorator: TextLineDecoration):
        pass

    @abstractmethod
    def group(self, grouper: Grouper):
        pass

    @abstractmethod
    def set_visible(self, vis_table: VisibilityTable):
        pass

    @abstractmethod
    def color(self, colorer: ColorTable, vector_gt: VectorGT):
        pass

    @abstractmethod
    def layer(self):
        pass

    @abstractmethod
    def combine_px_gts(self, comb: Combiner) -> Layer:
        pass

    @abstractmethod
    def mask(self, Image, Layer) -> Image:
        pass

    @abstractmethod
    def write(self, output_path):
        pass

    @abstractmethod
    def get_GT(self) -> Page:
        pass



