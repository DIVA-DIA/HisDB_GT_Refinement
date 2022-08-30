from pathlib import Path
from abc import abstractmethod
import logging

from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Sorter import Sorter
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Cropper import Cropper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Grouper import Grouper
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.IllustratorVisitor import Illustrator
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Resizer import Resizer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Colorer import Colorer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.Layerer import Layerer
from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitors.TextLineDecorator import TextLineDecorator
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.IO import Writer

logging.getLogger().setLevel(logging.INFO)

class GTBuilder():
    """The builder provides an interface for manipulating an instance of :class: `Page` class. It serves to construct
    the ground truth and is based on the builder design pattern. It improves code readability, complexity,
    and thus safety by replacing large constructors with many, different, optional input parameters with an auxiliary
    class. The auxiliary class is called Director and serves the methods provided by the builder in the desired order.
    If a new ground truth is to be built, developers:inside can write their own directors. Methods of the Builder can be
    called iteratively and are therefore superior to large constructors from this perspective as well. For example, if
    page objects of the vector GT are to be regrouped first and then sorted, this can be instructed in a few lines of
    code thanks to the builder pattern, see ClientExamples: RegionIllustratorDirector.py.
    """
    @abstractmethod
    def read(self, vector_gt_path: Path, px_gt_path: Path, orig_img: Path, vis_table: Path, col_table: Path):
        """Constructor Method
        :param vector_gt_path: path to the vector ground truth
        :type vector_gt_path: Path
        :param px_gt_path: path to the pixel-level ground truth
        :type px_gt_path: Path
        :param orig_img: path to the original image ground truth
        :type orig_img: Path
        :param vis_table: path to the visibility table to be applied to the ground truth :class: `Page`
        :type vis_table: VisibilityTable
        :param col_table: path to the color table to be applied to the ground truth :class: `Page`
        :type col_table: ColorTable
        """
        logging.info("Reading the ground truth files...")

    @abstractmethod
    def crop(self, cropper: Cropper):
        """Visit the Page with the :class: `Cropper` given.
        :param cropper: crop the pages image :class: `Image`, vector-gt :class: `VectorGT` and pixel-level-gt :class:
        `PixelLevelGT` according to the cropper's implementation.
        :type cropper: Cropper
        """
        logging.info("Cropping the ground truth...")

    def resize(self, resizer: Resizer):
        """Visit the Page with the :class: `Resizer` given.
        :param resizer: resize the pages image :class: `Image`, vector-gt :class: `VectorGT` and pixel-level-gt :class:
        `PixelLevelGT` according to the resizer's :class: `Resizer` implementation.
        :type resizer: Resizer
        """
        logging.info("Resizing the ground truth...")

    @abstractmethod
    def decorate(self, decorator: TextLineDecorator):
        """Visit the Page with the :class: `TextLineDecorator` given.
        :param resizer: decorate the pages image :class: `Image`, vector-gt :class: `VectorGT` and pixel-level-gt :class:
        `PixelLevelGT` according to the decorator's :class: `TextLineDecorator` implementation.
        :type resizer: TextLineDecorator
        """
        logging.info("Decorating the vector objects...")

    @abstractmethod
    def group(self, grouper: Grouper):
        """Visit the Page with the :class: `Grouper` given.
        :param grouper: group the pages image :class: `Image`, vector-gt :class: `VectorGT` and pixel-level-gt :class:
        `PixelLevelGT` according to the grouper's :class: `Grouper` implementation.
        :type grouper: Grouper
        """
        logging.info("(Re-)Grouping the vector objects...")

    @abstractmethod
    def sort(self, sorter: Sorter):
        """Visit the Page with the :class: `Sorter` given.
        :param grouper: sort the pages image :class: `Image`, vector-gt :class: `VectorGT` and pixel-level-gt :class:
        `PixelLevelGT` according to the sorter's :class: `Sorter` implementation.
        :type grouper: Sorter
        """
        logging.info("Sorting the vector objects...")

    @abstractmethod
    def set_visible(self):
        logging.info("Setting the different different vector objects to visible according to the Visibility Table...")

    @abstractmethod
    def set_color(self, colorer: Colorer = Colorer()):
        """ Set the color of both the vector_gt objects and the vector_gt."""
        logging.info("Setting the different color of each layout class in LayoutClasses...")

    @abstractmethod
    def layer(self, layerer: Layerer):
        """Visit the Page with the :class: `Layerer` given.
        :param layerer: combines the two ground-truths vector-gt :class: `VectorGT` and pixel-level-gt :class:`PixelLevelGT` and
        stores the newly generated pixel-based ground-truth based on the Layerer's implementation in the page :class:`Page`.
        :type layerer: Layerer
        """
        logging.info("Converting the VectorGT to layers in a new PixelLevelGT...")

    @abstractmethod
    def illustrate(self, illustrator: Illustrator):
        """Visit the Page with the :class: `Illustrator` given.
        :param illustrator: illustrate the pages image :class: `Image`, vector-gt :class: `VectorGT` and pixel-level-gt :class:
        `PixelLevelGT` according to the illustrator's :class: `Illustrator` implementation.
        :type illustrator: Illustrator
        """
        logging.info("Illustrate the ground_truths for debugging and illustrating purposes...")

    @abstractmethod
    def write(self, output_path: Path):
        """Visit the Page with the :class: `Writer` given.
        :param output_path: writes the pages image :class: `Image`, vector-gt :class: `VectorGT` and pixel-level-gt :class:
        `PixelLevelGT` to the :class: `Path` out_put_path to the format :class: `Writer`.
        :type output_path: Path
        """
        logging.info("Writing the new PixelLevelGT and all the visible VectorObjects to the given destination...")

    @abstractmethod
    def get_GT(self) -> Page:
        """ Get the new ground truth
        :return: Return the modified page :class: `Page`
        :rtype: Page
        """
        pass




