"""
# Graphy.
/src/graphy_detroix23/modules/graphics.py

Helper functions and classes for `pyxel`.
"""

import math

import pyxel

from graphy_detroix23.modules import defaults

class Colors:
    """
    # `Colors` of `pyxel`.

    Pointless, use `pyxel.COLOR_*` instead.
    """
    BLACK: int = 0
    DARK_BLUE: int = 1
    VIOLET: int = 2
    CYAN: int = 3
    BROWN: int = 4
    BLUE: int = 5
    LIGHT_BLUE: int = 6
    WHITE: int = 7
    MAGENTA: int = 8
    ORANGE: int = 9
    YELLOW: int = 10
    LIME: int = 11
    AZURE: int = 12
    GREY: int = 13
    PINK: int = 14
    BEIGE: int = 15


class Sprite:
    """
    # `Sprite` named tuple.
    Info of a sprite for drawing and for the `.pyxres` file.
    """
    image: int
    position: tuple[int, int]
    size: tuple[int, int]
    colkey: int
    offset: tuple[float, float]

    def __init__(
        self,
        image: int,
        position: tuple[int, int],
        size: tuple[int, int],
        colkey: int,
        offset: tuple[float, float] = (0.0, 0.0),
        
    ) -> None:
        self.image = image    
        self.position = position
        self.size = size
        self.colkey = colkey
        self.offset = offset


SPRITE_ARROW: Sprite = Sprite(
    0,
    (0, 16),
    (16, 16),
    defaults.COLKEY,
    (-8.0, -8.0),
)

def signum(number: float | int) -> int:
    """
    Returns 1, -1, 0, according to the sign of `number`
    """
    if number == 0:
        return 0
    elif number < 0:
        return -1
    else:
        return 1

def clip(number: float, minimum: float | None = None, maximum: float | None = None) -> float:
    """
    Clip the given `number` between `minimum` and `maximum`.
    """
    if minimum is not None and number < minimum:
        return minimum
    
    if maximum is not None and number > maximum:
        return maximum
    
    return number

def justify(string: str, total_length: int, fill: str = ' ') -> str:
    """
    Add spaces to the right of the `string` to match the `total_length`.
    """
    delta: int = total_length - len(string)
    if delta < 1:
        return string
    
    return string + fill * delta

def arrow(
    x1: float, 
    y1: float, 
    x2: float, 
    y2: float,
    color: int,
    scale: float = 1.0,
    shorten: float = 0.0,
    shift: float = 0.0
) -> None:
    """
    Draw an arrow from P1(`x1`, `y1`) to P2(`x2`, `y2`).
    """
    point: tuple[float, float] = (x2 - x1, y2 - y1)
    length: float = math.sqrt(point[0] * point[0] + point[1] * point[1])
    # Angle of the arrow from P1 to P2
    angle: float
    if length > 0:
        if signum(point[1]) == 0:
            angle = math.acos(point[0] / length)
        else:
            angle = signum(point[1]) * math.acos(point[0] / length)
    else:
        angle = 0

    # Unit vector
    vector: tuple[float, float] = (math.cos(angle), math.sin(angle))
    arrow_distance: float = length - shorten if length > shorten else 0.0
    arrow_position: tuple[float, float] = (x1 + vector[0] * arrow_distance, y1 + vector[1] * arrow_distance)

    pyxel.blt(
        arrow_position[0] + SPRITE_ARROW.offset[0] + shift * vector[1],
        arrow_position[1] + SPRITE_ARROW.offset[1] - shift * vector[0],
        SPRITE_ARROW.image,
        SPRITE_ARROW.position[0],
        SPRITE_ARROW.position[1],
        SPRITE_ARROW.size[0],
        SPRITE_ARROW.size[1],
        SPRITE_ARROW.colkey,
        scale=scale,
        rotate=math.degrees(angle) + 90.0,
    )
    pyxel.line(
        x1 + shift * vector[1], 
        y1 - shift * vector[0], 
        arrow_position[0] + shift * vector[1], 
        arrow_position[1] - shift * vector[0], 
        color
    )

def jagged_line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    jag: float,
    color: int,
    shift: float = 0.0
) -> None:
    """
    Draw a jagged line, with `jag`s.
    """
    vector: tuple[float, float] = (x2 - x1, y2 - y1)
    length: float = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    normal: tuple[float, float] = (
        (vector[0] / length, vector[1] / length)
        if length > 0
        else (0.0, 0.0) 
    )
    t: float = shift

    while t + 2 * jag < length:
        pyxel.line(
            x1 + t * normal[0],
            y1 + t * normal[1],
            x1 + (t + jag) * normal[0],
            y1 + (t + jag) * normal[1],
            color,
        )
        t += 2 * jag

    pyxel.line(
        x1 + t * normal[0],
        y1 + t * normal[1],
        x1 + clip(t + jag, maximum=length) * normal[0],
        y1 + clip(t + jag, maximum=length) * normal[1],
        color,
    )

    