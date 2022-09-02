from abc import abstractmethod
from pathlib import Path

from GTRefiner.Builder import Builder
from GTRefiner.GTRepresentation.Table import ColorTable, VisibilityTable


class Director:

    @abstractmethod
    def make(self):
        pass


class Prototyper(Director):
    """ Creates prototypes of the given ColorTable, VisibilityTable, Paths, and Builder and shows it. Once pleased,
    the client can should use the factory :class: `Factory` class.
    """

    def __init__(self, builder: Builder, color_table: ColorTable, vis_table: VisibilityTable,
                   vector_gt: Path, px_gt: Path, ori_img: Path):
        pass

class Factory(Director):
    """ Calls the given Builder on all the GT_files in the root directory.
    """
    def __init__(self, builder: Builder, color_table: ColorTable, vis_table: VisibilityTable,
                   root_directory: Path):
        pass