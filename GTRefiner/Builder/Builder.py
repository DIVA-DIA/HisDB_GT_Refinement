from pathlib import Path
from abc import abstractmethod
import logging

from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Cropper import Cropper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Grouper import Grouper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Resizer import Resizer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Colorer import Colorer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Combiner import Combiner
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.TextLineDecorator import TextLineDecorator
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer

# TODO: Director soll verantwortung für ablauf und instanziierung der Buildingtools übernehmen.

logging.getLogger().setLevel(logging.INFO)

class GTBuilder():

    # TODO: decorator @logging -> tutorial nachschauen.
    @abstractmethod
    def read(self, vector_gt_path: Path, px_gt_path: Path, orig_img: Path, vis_table: Path, col_table: Path):
        logging.info("Reading the ground truth files...")

    @abstractmethod
    def crop(self, cropper: Cropper):
        logging.info("Cropping the ground truth...")

    def resize(self, resizer: Resizer):
        logging.info("Resizing the ground truth...")

    @abstractmethod
    def decorate(self, decorator: TextLineDecorator):
        logging.info("Decorating the vector objects...")

    @abstractmethod
    def group(self, grouper: Grouper):
        logging.info("(Re-)Grouping the vector objects...")

    @abstractmethod
    def set_visible(self):
        logging.info("Setting the different different vector objects to visible according to the Visibility Table")

    @abstractmethod
    def set_color(self, colorer: Colorer = Colorer()):
        """ Set the color of both the vector_gt objects and the vector_gt."""
        logging.info("Setting the different color of each layout class in LayoutClasses")

    @abstractmethod
    def combine(self, layerer: Combiner):
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




