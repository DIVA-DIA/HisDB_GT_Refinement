import json
from abc import abstractmethod
from pathlib import Path
from typing import Any, Dict, Tuple, List

from GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses


class Table():
    """ Provides the base class for layout class :class: `LayoutClasses` based dictionaries. Can be dumped to JSON file.
    :param table: Dictionary of layout classes
    :type table: Dict[LayoutClasses, Any]
    """

    @abstractmethod
    def __init__(self, table: Dict[LayoutClasses, Any]):
        self.table = table

    def to_json(self, file_path: Path = Path("../../Resources/some_table.json")):
        """ Dumps the the table to json file with a given file path.
        :param file_path: Output file path
        :type file_path: Path
        """
        json.dump(self.table, open(file_path, "w"), indent=4)

    def __getitem__(self, item):
        return self.table[item]


# TODO: Color soll eine method .toGIFpalette() haben. ->
class ColorTable(Table):
    """ Defines the colors for the ground truth objects (texelements of the vector gt, levels of the
    pixel gt). If you want to implement iterating or all different colors you need to provide a list of colors for the
    target LayoutClass. Compare with the color tables in the Ressources/ColorTables/ directory.
    :param table: Color table
    :type table: Dict[LayoutClasses, List[Tuple]
    """

    def __init__(self, table: Dict[LayoutClasses, List[Tuple]]):

        super().__init__(table)


class VisibilityTable(Table):
    """Defines the visibility for the ground truth objects (texelements of the vector gt, levels of the
    pixel gt).
    :param table: Visibility table
    :type table: Dict[LayoutClasses, bool]
    """
    def __init__(self, table: Dict[LayoutClasses, bool]):
        super().__init__(table)
