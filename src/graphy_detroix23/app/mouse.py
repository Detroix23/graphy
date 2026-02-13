"""
# Graphy.
/src/graphy_detroix23/app/mouse.py
"""

import enum
from typing import TYPE_CHECKING

import pyxel

if TYPE_CHECKING:
    from graphy_detroix23.app import base
from graphy_detroix23.modules import (
    defaults,
    graphics,
)

class State(enum.Enum):
    """
    # `State` of the mouse cursor.
    - `SELECT`,
    - `HOLD`,
    - `DRAW`.
    """
    SELECT = 0
    HOLD = 1
    DRAW = 2


class Mouse:
    """
    # `Mouse` track, graphics for the `App`.
    """
    SPRITE_SELECT: graphics.Sprite = graphics.Sprite(
        0,
        (16, 0),
        (16, 16),
        defaults.COLKEY,
        (8.0, 8.0),
    )
    SPRITE_HOLD: graphics.Sprite = graphics.Sprite(
        0,
        (32, 0),
        (16, 16),
        defaults.COLKEY,
        (0.0, 0.0),
    )
    SPRITE_DRAW: graphics.Sprite = graphics.Sprite(
        0,
        (48, 0),
        (16, 16),
        defaults.COLKEY,
        (8.0, 8.0),
    )

    parent: 'base.App'
    shown: bool
    state: State
    size: float

    def __init__(self, parent: 'base.App') -> None:
        self.parent = parent
        self.shown = True
        self.state = State.SELECT
        self.size = 2.0

    def draw(self) -> None:
        """
        Draw the cursor, according to the state.
        """
        position: tuple[int, int]

        if self.state == State.HOLD:
            position = self.SPRITE_HOLD.position
            pyxel.blt(
                pyxel.mouse_x + self.SPRITE_HOLD.offset[0],
                pyxel.mouse_y + self.SPRITE_HOLD.offset[1],
                self.SPRITE_HOLD.image,
                position[0],
                position[1],
                self.SPRITE_HOLD.size[0],
                self.SPRITE_HOLD.size[1],
                self.SPRITE_HOLD.colkey,
                scale=self.size,
            )
        
        elif self.state == State.DRAW:
            position = self.SPRITE_DRAW.position
            pyxel.blt(
                pyxel.mouse_x + self.SPRITE_DRAW.offset[0],
                pyxel.mouse_y + self.SPRITE_DRAW.offset[1],
                self.SPRITE_DRAW.image,
                position[0],
                position[1],
                self.SPRITE_DRAW.size[0],
                self.SPRITE_DRAW.size[1],
                self.SPRITE_DRAW.colkey,
                scale=self.size,
            )
        
        else:
            position = self.SPRITE_SELECT.position
            pyxel.blt(
                pyxel.mouse_x + self.SPRITE_SELECT.offset[0],
                pyxel.mouse_y + self.SPRITE_SELECT.offset[1],
                self.SPRITE_SELECT.image,
                position[0],
                position[1],
                self.SPRITE_SELECT.size[0],
                self.SPRITE_SELECT.size[1],
                self.SPRITE_SELECT.colkey,
                scale=self.size,
            )
    