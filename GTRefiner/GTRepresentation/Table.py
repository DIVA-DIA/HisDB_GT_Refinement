from abc import abstractmethod
from typing import Any, Dict

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses


class Table():

    @abstractmethod
    def __init__(self, table: Dict[LayoutClasses, Any]):
        self.table = table


class ColorTable():
    pass


class VisibilityTable():
    pass
