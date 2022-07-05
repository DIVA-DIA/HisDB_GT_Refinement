from pathlib import Path
from PIL import Image
from abc import abstractmethod
import logging

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
        logging.info("Reading the ground truth files...")

    @abstractmethod
    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        logging.info("Cropping the ground truth...")

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        logging.info("Resizing the ground truth...")

    @abstractmethod
    def decorate(self, decorator: TextLineDecoration):
        logging.info("Decorating the vector objects...")

    @abstractmethod
    def group(self, grouper: Grouper):
        logging.info("(Re-)Grouping the vector objects...")

    @abstractmethod
    def set_visible(self, vis_table: VisibilityTable):
        logging.info("Setting the different different vector objects to visible according to the Visibility Table")

    @abstractmethod
    def color(self, colorer: ColorTable, vector_gt: VectorGT):
        logging.info("Setting the different color of each layout class in LayoutClasses")

    @abstractmethod
    def layer(self):
        logging.info("Converting the VectorGT to layers in a new PixelLevelGT")

    @abstractmethod
    def combine_px_gts(self, comb: Combiner) -> Layer:
        logging.info("Combine the new PixelLevelGT with the original PixelLevelGT")

    # @abstractmethod
    # def mask(self, Image, Layer) -> Image:
    #     logging.info("Combine the new PixelLevelGT with the original PixelLevelGT")

    @abstractmethod
    def write(self, output_path):
        logging.info("Writing the new PixelLevelGT and all the visible VectorObjects to the given destination.")

    @abstractmethod
    def get_GT(self) -> Page:
        pass



