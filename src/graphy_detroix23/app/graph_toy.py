"""
# Graphy.
/src/graphy_detroix23/app/graph_toy.py
"""

import pyxel

import structures_detroix23 as structures

from graphy_detroix23.modules import defaults

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
    size: float

    def __init__(
        self, 
        name: str, 
        previous: dict[structures.nodes.Node, float] | None = None, 
        next: dict[structures.nodes.Node, float] | None = None
    ) -> None:
        super().__init__(name, previous, next)
        self.position = (100.0, 100.0)
        self.size = 1.0

    def __repr__(self) -> str:
        return f"Node(name={self._name}, id={self._id}, previous={self._previous}, \
next={self._next}, position={self.position}, size={self.size})"

    def draw(self) -> None:
        """
        Draw this `NodeToy`.
        """
        pyxel.blt(
            self.position[0],
            self.position[1],
            self.SPRITE_IMAGE,
            self.SPRITE_POSITION[0],
            self.SPRITE_POSITION[1],
            self.SPRITE_SIZE[0],
            self.SPRITE_SIZE[1],
            self.SPRITE_COLKEY,
            scale=self.size,
        )

class GraphToy:
    """
    # `GraphToy` is the main character.
    """
    _register: dict[str, NodeToy]

    def __init__(self) -> None:
        self._register = dict()
    
    def add(self, name: str) -> None:
        """
        Add a new `Node` with a `name` and no neighbors to the `_register`.
        """
        self._register[name] = NodeToy(name)
    
    def remove(self, name: str) -> NodeToy | None:
        """
        Remove a `Node` `name` from the `_register`.   
        Returns the removed `Node` or `None` if didn't existed.
        """
        return self._register.pop(name, None)

    def draw(self) -> None:
        """
        Draw all the nodes of the graph.
        """
        for node in self._register.values():
            node.draw()
    
    def display_register(self) -> str:
        """
        Get a formatted string of the `_register`.
        """
        return "GraphToy._register={\n  " + ", \n  ".join([f"{name}: {repr(node)}" for name, node in self._register.items()]) + "\n}"
        