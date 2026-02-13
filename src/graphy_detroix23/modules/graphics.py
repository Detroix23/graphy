"""
# Graphy.
/src/graphy_detroix23/modules/graphics.py

Helper functions and classes for `pyxel`.
"""

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

    