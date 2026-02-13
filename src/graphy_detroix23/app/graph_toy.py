"""
# Graphy.
/src/graphy_detroix23/app/graph_toy.py
"""

from typing import TYPE_CHECKING

import pyxel

if TYPE_CHECKING:
    from graphy_detroix23.app import base
from graphy_detroix23.modules import graphics
from graphy_detroix23.app import mouse, node_toy

class GraphToy:
    """
    # `GraphToy` is the main character.
    """
    parent: 'base.App'
    _register: dict[str, node_toy.NodeToy]
    selected: node_toy.NodeToy | None
    arc_origin: node_toy.NodeToy | None

    def __init__(self, parent: 'base.App') -> None:
        self.parent = parent
        self._register = dict()
        self.selected = None
        self.arc_origin = None
    
    def __getitem__(self, name: str) -> node_toy.NodeToy:
        """
        Return a `node_toy.NodeToy` named `name`. Raise if it doesn't exist.
        """
        return self._register[name]

    def add(self, name: str) -> None:
        """
        Add a new `Node` with a `name` and no neighbors to the `_register`.
        """
        self._register[name] = node_toy.NodeToy(name)
    
    def remove(self, name: str) -> node_toy.NodeToy | None:
        """
        Remove a `Node` `name` from the `_register`.   
        Returns the removed `Node` or `None` if didn't existed.
        """
        return self._register.pop(name, None)

    def default_position(self, radius: float) -> None:
        """
        Spreads the nodes.
        """
        angle: float = 0.0
        increment: float = 360.0 / len(self._register) 
        center: tuple[float, float] = (pyxel.width / 2, pyxel.height / 2)

        for node in self._register.values():
            node.position = (
                pyxel.cos(angle) * radius + center[0],
                pyxel.sin(angle) * radius + center[1],
            )
            angle += increment

    def set_selection(self, node: node_toy.NodeToy | None) -> None:
        """
        Update the selection attribute `selected`.
        Also updates the mouse.
        """
        self.selected = node
        if node is None:
            self.parent.mouse_handler.state = mouse.State.SELECT
        else:
            self.parent.mouse_handler.state = mouse.State.HOLD

    def set_arc_origin(self, node: node_toy.NodeToy | None) -> None:
        """
        Update the selection attribute `selected`.
        Also updates the mouse.
        """ 
        self.arc_origin = node
        if node is None:
            self.parent.mouse_handler.state = mouse.State.SELECT
        else:
            self.parent.mouse_handler.state = mouse.State.DRAW



    def select_node(self, position: tuple[float, float]) -> node_toy.NodeToy | None:
        """
        Return a `node_toy.NodeToy` if there is one under on `position`, `None` else.
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
                end: node_toy.NodeToy | None = self.select_node((pyxel.mouse_x, pyxel.mouse_y))
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
            jag: float = 10.0

            graphics.jagged_line(
                self.arc_origin.position[0],
                self.arc_origin.position[1],
                pyxel.mouse_x,
                pyxel.mouse_y,
                jag=jag,
                color=pyxel.COLOR_LIME,
                shift=pyxel.frame_count % int(jag * 2)
            )

            
        for node in self._register.values():
            node.draw()
    
    def display_register(self) -> str:
        """
        Get a formatted string of the `_register`.
        """
        return "GraphToy._register: \n" + ", \n".join([f"{name}: {node.display('  ')}" for name, node in self._register.items()])
        