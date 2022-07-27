import json
from pathlib import Path
from typing import Dict

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses

color_table: Dict = {
    "BACKGROUND": [(0, 0, 0)],
    # base_classes
    "COMMENT": [(255, 0, 0), (244, 0, 0)],
    "DECORATION": [(0, 255, 0)],
    "COMMENT_AND_DECORATION": [(255, 255, 0)],
    "MAINTEXT": [(0, 0, 255)],
    "COMMENT_AND_MAINTEXT": [(255, 0, 255)],
    "MAINTEXT_AND_DECORATION": [(0, 255, 255)],
    "MAINTEXT_AND_DECORATION_AND_COMMENT": [(255, 255, 255)],
    # decorations
    "ASCENDER": [(250, 120, 120),(20, 120, 212),(20, 212, 120)],
    "XREGION": [(120, 250, 120)],
    "DESCENDER": [(120, 120, 250)],
    "BASELINE": [(30, 100, 200)],
    "TOPLINE": [(100, 30, 200)],
    "HEAD": [(100, 100, 100)],
    "TAIL": [(100, 100, 100)],
    "TEXT_REGION": [(100, 100, 100)],
    # # coloring_strategy for base_classes
    # "ColoingStrategy:": {"MAINTEXT": "Unicolor", "COMMENT": "Unicolor", "DECORATION": "Unicolor"}
}

vis_table: Dict = {
    "BACKGROUND": False,
    "COMMENT": True,
    "DECORATION": True,
    "COMMENT_AND_DECORATION": True,
    "MAINTEXT": True,
    "COMMENT_AND_MAINTEXT": True,
    "MAINTEXT_AND_DECORATION": True,
    "MAINTEXT_AND_DECORATION_AND_COMMENT": True,
    "ASCENDER": True,
    "XREGION": True,
    "DESCENDER": True,
    "BASELINE": True,
    "TOPLINE": True,
    "HEAD": True,
    "TAIL": True,
    "TEXT_REGION": True,
}
if __name__ == '__main__':
    # write to json
    file_path: Path = Path("../../Resources/ColorTables/color_table_with_color_lists_2.json")
    json.dump(color_table, open(file_path, "w"), indent=4)

    # # read (old) color table json and convert to {LayoutClasses: Tuple}
    # data = json.load(open(file_path))
    # data = {LayoutClasses.str_to_enum(k): tuple(v) for (k,v) in data.items()}
    # print(data)
    # #
    # # read visibility table
    # data = json.load(open(file_path))
    # data = {LayoutClasses.str_to_enum(k): v for (k,v) in data.items()}
    # print(data)

    # read color table json and convert to {LayoutClasses: Tuple}
    data = json.load(open(file_path))
    data = {LayoutClasses.str_to_enum(k): list(tuple(v) for v in v) for (k, v) in data.items()}
    #data = {LayoutClasses.str_to_enum(k): list(tuple(tup) for tup in v) for v in (k,v) in data.items()}
    print(data)
