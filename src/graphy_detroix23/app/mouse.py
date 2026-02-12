"""
# Graphy.
/src/graphy_detroix23/app/mouse.py
"""

import enum
import pyxel

from graphy_detroix23.modules import defaults

class State(enum.Enum):
    """
    # `State` of the mouse cursor.
    """
    SELECT = 0
    HOLD = 1


class Mouse:
    """
    # `Mouse` track, graphics for the `App`.
    """
    SELECT_POSITION: tuple[int, int] = (16, 0)
    HOLD_POSITION: tuple[int, int] = (16, 0)
    SPRITE_SIZE: tuple[int, int] = (16, 16)
    SPRITE_IMAGE: int = 0
    SPRITE_COLKEY: int = defaults.COLKEY

    shown: bool
    state: State
    size: float

    def __init__(self) -> None:
        self.shown = True
        self.state = State.SELECT
        self.size = 2.0

    def draw(self) -> None:
        """
        Draw the cursor, according to the state.
        """
        position: tuple[int, int]
        if self.state == State.SELECT:
            position = self.SELECT_POSITION
        else:
            position = self.HOLD_POSITION

        pyxel.blt(
            pyxel.mouse_x,
            pyxel.mouse_y,
            self.SPRITE_IMAGE,
            position[0],
            position[1],
            self.SPRITE_SIZE[0],
            self.SPRITE_SIZE[1],
            self.SPRITE_COLKEY,
            scale=self.size,
        )
    