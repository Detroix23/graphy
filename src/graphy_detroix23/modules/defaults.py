"""
# Graphy.
/src/graphy_detroix23/modules/paths.py
"""

import pathlib
from typing import Final
import pyxel


COLKEY: Final[int] = 8

RESOURCE_FILE: Final[pathlib.Path] = pathlib.Path("../../../resources/graphy.pyxres")

FONT_BIG_BLUE_FILE: Final[pathlib.Path] = pathlib.Path("resources/big_blue_font/BigBlueTermPlusNerdFont-Regular.ttf")
FONT_BIG_BLUE_SIZE: int = 12
FONT_BIG_BLUE = pyxel.Font(str(FONT_BIG_BLUE_FILE), FONT_BIG_BLUE_SIZE)

SCALE_ALL: Final[list[int]] = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
SCALE_ALL_2: Final[list[int]] = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
SCALE_MAJOR: Final[list[int]] = [0, 2, 2, 1, 2, 2, 2, 1]
SCALE_MAJOR_2: Final[list[int]] = [0, 2, 2, 1, 2, 2, 2, 1, -1, -2, -2, -2, -1, -2, -2]
SCALE_BOOGIE: Final[list[int]] = [0, 3, 2, 1, 1, 3, 2]
SCALE_BOOGIE_2: Final[list[int]] = [0, 3, 2, 1, 1, 3, 2, -2, -3, -1, -1, -2]
