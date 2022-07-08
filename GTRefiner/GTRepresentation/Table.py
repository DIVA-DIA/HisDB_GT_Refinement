import json
from abc import abstractmethod
from pathlib import Path
from typing import Any, Dict, Tuple

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses


class Table():

    @abstractmethod
    def __init__(self, table: Dict[LayoutClasses, Any]):
        self.table = table

    def to_json(self, file_path: Path = Path("../../Resources/some_table.json")):
        json.dump(self.table, open(file_path, "w"), indent=4)

    def __getitem__(self, item):
        return self.table[item]


# TODO: Color soll eine method .toGIFpalette() haben. ->
class ColorTable(Table):

    def __init__(self, table: Dict[LayoutClasses, Tuple]):
        super().__init__(table)


class VisibilityTable(Table):

    def __init__(self, table: Dict[LayoutClasses, bool]):
        super().__init__(table)
