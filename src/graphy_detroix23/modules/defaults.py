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
FONT_BIG_BLUE = pyxel.Font(str(FONT_BIG_BLUE_FILE), 18)

