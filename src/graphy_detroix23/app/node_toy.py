"""
# Graphy.
/src/graphy_detroix23/app/node_toy.py
"""

import pyxel

import structures_detroix23 as structures
from graphy_detroix23.modules import defaults, graphics

class NodeToy(structures.nodes.Node):
    """
    # `NodeToy` wrapper for `Node`.
    Contains a graphical and spacial state.
    """
    SPRITE_POSITION: tuple[int, int] = (0, 0)
    SPRITE_SIZE: tuple[int, int] = (16, 16)
    SPRITE_IMAGE: int = 0
    SPRITE_COLKEY: int = defaults.COLKEY

    position: tuple[float, float]
    # Actual screen radius, in pixels.
    radius: float
    # Sprite scale.
    scale: float
    is_selected: bool

    def __init__(
        self,
        name: str, 
        previous: dict[structures.nodes.Node, float] | None = None, 
        next: dict[structures.nodes.Node, float] | None = None
    ) -> None:
        """
        Initialize the `NodeToy` from `Node`.
        """
        super().__init__(name, previous, next)
        self.position = (100.0, 100.0)
        self.radius = 32
        self.scale = 1.0
        self.is_selected = False

    def __repr__(self) -> str:
        return f"Node(name={self._name}, id={self._id}, previous={self._previous}, \
next={self._next}, position={self.position}, scale={self.scale}, radius={self.radius})"

    def draw(self, show_weights: bool) -> None:
        """
        Draw this `NodeToy`.
        """
        scale: float = self.radius / self.SPRITE_SIZE[0] * self.scale

        if self.is_selected:
            pyxel.dither(0.8)

        # Arcs.
        for neighbor, weight in self.get_next().items():
            if isinstance(neighbor, NodeToy):
                graphics.arrow(
                    self.position[0],
                    self.position[1],
                    neighbor.position[0],
                    neighbor.position[1],
                    color=pyxel.COLOR_LIGHT_BLUE,
                    scale=1.0,
                    shorten=neighbor.radius,
                    shift=5.0,
                )

                if show_weights:
                    pyxel.text(
                        (self.position[0] + neighbor.position[0]) / 2,
                        (self.position[1] + neighbor.position[1]) / 2,
                        str(weight),
                        col=pyxel.COLOR_NAVY,
                        font=defaults.FONT_BIG_BLUE,
                    )

        # Main circle of the node.
        pyxel.blt(
            self.position[0] - self.SPRITE_SIZE[0] // 2,
            self.position[1] - self.SPRITE_SIZE[1] // 2,
            self.SPRITE_IMAGE,
            self.SPRITE_POSITION[0],
            self.SPRITE_POSITION[1],
            self.SPRITE_SIZE[0],
            self.SPRITE_SIZE[1],
            self.SPRITE_COLKEY,
            scale=scale,
        )

        # Label.
        pyxel.text(
            self.position[0] - self.SPRITE_SIZE[0] // 2 + 4,
            self.position[1] - self.SPRITE_SIZE[1] // 2 + 2,
            self.get_name(),
            pyxel.COLOR_DARK_BLUE,
            defaults.FONT_BIG_BLUE,
        )

        pyxel.dither(1.0)