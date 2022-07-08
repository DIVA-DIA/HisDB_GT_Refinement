import json
from pathlib import Path
from typing import Dict

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses

color_table: Dict = {
    "BACKGROUND": (0, 0, 0),
    "COMMENT": (255, 0, 0),
    "DECORATION": (0, 255, 0),
    "COMMENT_AND_DECORATION": (255, 255, 0),
    "MAINTEXT": (0, 0, 255),
    "COMMENT_AND_MAINTEXT": (255, 0, 255),
    "MAINTEXT_AND_DECORATION": (0, 255, 255),
    "MAINTEXT_AND_DECORATION_AND_COMMENT": (255, 255, 255),
    "ASCENDER": (250, 120, 120),
    "XREGION": (120, 250, 120),
    "DESCENDER": (120, 120, 250),
    "BASELINE": (30, 100, 200),
    "TOPLINE": (100, 30, 200),
    "HEAD": (100, 100, 100),
    "TAIL": (100, 100, 100),
    "TEXT_REGIONS": (100, 100, 100),
}

if __name__ == '__main__':

    # write to json
    file_path: Path = Path("../../Resources/color_table.json")
    json.dump(color_table, open(file_path, "w"), indent=4)

    # read json and convert to {LayoutClasses: Tuple}
    data = json.load(open(file_path))
    data = {LayoutClasses.str_to_enum(k): tuple(v) for (k,v) in data.items()}
    print(data)


