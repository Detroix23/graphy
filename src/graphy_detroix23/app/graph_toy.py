"""
# Graphy.
/src/graphy_detroix23/app/graph_toy.py
"""

from typing import TYPE_CHECKING

import pyxel

if TYPE_CHECKING:
    from graphy_detroix23.app import base
import structures_detroix23 as structures
from graphy_detroix23.modules import defaults, graphics
from graphy_detroix23.app import mouse

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

    def __repr__(self) -> str:
        return f"Node(name={self._name}, id={self._id}, previous={self._previous}, \
next={self._next}, position={self.position}, scale={self.scale}, radius={self.radius})"

    def draw(self) -> None:
        """
        Draw this `NodeToy`.
        """
        scale: float = self.radius / self.SPRITE_SIZE[0] * self.scale

        # Arcs.
        for neighbor in self.get_next().keys():
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
            self.position[0] - self.SPRITE_SIZE[0] // 2 + 3,
            self.position[1] - self.SPRITE_SIZE[1] // 2,
            self.get_name(),
            pyxel.COLOR_DARK_BLUE,
            defaults.FONT_BIG_BLUE,
        )


class GraphToy:
    """
    # `GraphToy` is the main character.
    """
    parent: 'base.App'
    _register: dict[str, NodeToy]
    selected: NodeToy | None
    arc_origin: NodeToy | None

    def __init__(self, parent: 'base.App') -> None:
        self.parent = parent
        self._register = dict()
        self.selected = None
        self.arc_origin = None
    
    def __getitem__(self, name: str) -> NodeToy:
        """
        Return a `NodeToy` named `name`. Raise if it doesn't exist.
        """
        return self._register[name]

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

    def set_selection(self, node: NodeToy | None) -> None:
        """
        Update the selection attribute `selected`.
        Also updates the mouse.
        """
        self.selected = node
        if node is None:
            self.parent.mouse_handler.state = mouse.State.SELECT
        else:
            self.parent.mouse_handler.state = mouse.State.HOLD

    def set_arc_origin(self, node: NodeToy | None) -> None:
        """
        Update the selection attribute `selected`.
        Also updates the mouse.
        """ 
        self.arc_origin = node
        if node is None:
            self.parent.mouse_handler.state = mouse.State.SELECT
        else:
            self.parent.mouse_handler.state = mouse.State.DRAW



    def select_node(self, position: tuple[float, float]) -> NodeToy | None:
        """
        Return a `NodeToy` if there is one under on `position`, `None` else.
        """
        for node in self._register.values():
            # Check if in radius.
            if ((position[0] - node.position[0]) ** 2 
                + (position[1] - node.position[1]) ** 2 
                <= node.radius ** 2
            ):
                return node
             
        return None 

    def node_selection(self) -> None:
        """
        Handles left mouse click and `NodeToy`s moving.
        """
        # Selection
        if self.selected is None:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.set_selection(self.select_node((pyxel.mouse_x, pyxel.mouse_y)))
        
        else:
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                self.set_selection(None)
        
        # Moving the selection.
        if self.selected is not None:
            self.selected.position = (pyxel.mouse_x, pyxel.mouse_y)

    def arcs_tool(self) -> None:
        """
        Handles right mouse click to create new connection between `NodeToy`s.
        """
        if self.arc_origin is None:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                self.set_arc_origin(self.select_node((pyxel.mouse_x, pyxel.mouse_y)))

        else:
            if pyxel.btnr(pyxel.MOUSE_BUTTON_RIGHT):
                end: NodeToy | None = self.select_node((pyxel.mouse_x, pyxel.mouse_y))
                if end is not None:
                    if end in self.arc_origin.get_next():
                        self.arc_origin.remove_next(end)
                    else:
                        self.arc_origin.set_next(end, 1.0)


                self.set_arc_origin(None)

    def update(self) -> None:
        """
        Update positions, nodes, mouse.
        """
        self.node_selection()
        self.arcs_tool()
        
    def draw(self) -> None:
        """
        Draw all the nodes of the graph.
        """
        # Drawing arc
        if self.arc_origin is not None:
            pyxel.line(
                self.arc_origin.position[0],
                self.arc_origin.position[1],
                pyxel.mouse_x,
                pyxel.mouse_y,
                col=pyxel.COLOR_LIME,
            )

        for node in self._register.values():
            node.draw()
    
    def display_register(self) -> str:
        """
        Get a formatted string of the `_register`.
        """
        return "GraphToy._register={\n  " + ", \n  ".join([f"{name}: {repr(node)}" for name, node in self._register.items()]) + "\n}"
        