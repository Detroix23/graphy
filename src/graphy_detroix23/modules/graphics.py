"""
# Graphy.
/src/graphy_detroix23/modules/graphics.py

Helper functions and classes for `pyxel`.
"""

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

    