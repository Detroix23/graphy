"""
# Graphy.
/src/graphy_detroix23/app/graph_toy.py
"""

from typing import TYPE_CHECKING

import pyxel

if TYPE_CHECKING:
    from graphy_detroix23.app import base
from graphy_detroix23.modules import defaults, graphics, sound
from graphy_detroix23.app import mouse, node_toy

class GraphToy:
    """
    # `GraphToy` is the main character.
    """
    parent: 'base.App'
    _register: dict[str, node_toy.NodeToy]
    selected: node_toy.NodeToy | None
    arc_origin: node_toy.NodeToy | None
    _last_added: str | None
    show_weights: bool

    sound_node_creation: sound.Incrementing
    sound_node_removal: sound.Incrementing
    sound_node_connection: sound.Incrementing
    sound_node_disconnection: sound.Incrementing


    def __init__(self, parent: 'base.App') -> None:
        self.parent = parent
        self._register = dict()
        self.selected = None
        self.arc_origin = None
        self._last_added = None
        self.show_weights = True

        self.sound_node_creation = sound.Incrementing(
            channel=0, 
            tempo=180, 
            division=8, 
            length=100, 
            velocity=32, 
            start_note=sound.Note("C"), 
            scale=defaults.SCALE_BOOGIE_2,
        )
        self.sound_node_removal = sound.Incrementing(
            channel=0, 
            tempo=180, 
            division=8, 
            length=100, 
            velocity=32, 
            start_note=sound.Note("F", octave=-1), 
            scale=defaults.SCALE_MAJOR_2,
        )
        self.sound_node_connection = sound.Incrementing(
            channel=0, 
            tempo=180, 
            division=8, 
            length=100, 
            velocity=32, 
            start_note=sound.Note("E"), 
            scale=defaults.SCALE_ALL,
        )
        self.sound_node_disconnection = sound.Incrementing(
            channel=0, 
            tempo=180, 
            division=8, 
            length=100, 
            velocity=32, 
            start_note=sound.Note("A", octave=-1, signature=sound.Signature.FLAT), 
            scale=defaults.SCALE_ALL,
        )
        self.sound_node_connection_fail = sound.MML(
            channel=0,
            tempo=180,
            division=8,
            length=100,
            velocity=32,
            notes=[sound.Note("B", octave=-2, signature=sound.Signature.FLAT)]
        )

    def __getitem__(self, name: str) -> node_toy.NodeToy:
        """
        Return a `node_toy.NodeToy` named `name`. Raise if it doesn't exist.
        """
        return self._register[name]

    @property
    def card(self) -> int:
        """
        Returns the _Card_, or the number total of nodes.
        """
        return len(self._register)

    def toggle_weight_visibility(self) -> None:
        """
        Toggle on or off the `show_weight` boolean.
        """
        self.show_weights = not self.show_weights

    def add(
        self, 
        name: str, 
        position: tuple[float, float] = (0.0, 0.0),
    ) -> None:
        """
        Add a new `Node` with a `name` and no neighbors to the `_register`.
        """
        self._last_added = name
        node = node_toy.NodeToy(name)
        node.position = position
        self._register[name] = node
    
    def add_continuing(
        self, 
        position: tuple[float, float] = (0.0, 0.0)
    ) -> None:
        """
        Add a new `Node` and no neighbors to the `_register`.  
        Name is the following ASCII character after `_last_added`.
        """
        name: str = "A" if self._last_added is None else chr(ord(self._last_added) + 1)
        self.add(name, position)

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
        # Removes the hold selection.
        if self.selected is not None:
            self.selected.is_selected = False

        if node is None:
            self.parent.mouse_handler.state = mouse.State.SELECT
        else:
            self.parent.mouse_handler.state = mouse.State.HOLD
            node.is_selected = True

        self.selected = node

        return

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
            notes: list[str] = ["F", "A", "C", "E-"]
            pyxel.play(0, f"T120 L4 Q30 V8 {notes[int(pyxel.frame_count / 2) % 4]}")
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                self.set_selection(None)
        
        # Moving the selection.
        if self.selected is not None:
            self.selected.position = (
                graphics.clip(pyxel.mouse_x, minimum=0.0, maximum=pyxel.width), 
                graphics.clip(pyxel.mouse_y, minimum=0.0, maximum=pyxel.height)
            )

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
                        self.sound_node_disconnection.play()
                    else:
                        self.arc_origin.set_next(end, 1.0)
                        self.sound_node_connection.play()

                else:
                    self.sound_node_connection_fail.play()

                self.set_arc_origin(None)
            
            else:
                # Drawing.
                notes: list[str] = ["C", "E", "G", "<B-"]
                pyxel.play(0, f"T80 L1 Q100 V8 {notes[int(pyxel.frame_count / 2) % 4]}")

    def node_creation(self) -> None:
        """
        Handles middle mouse button to create a new node, named automatically.
        """
        if pyxel.btnp(pyxel.MOUSE_BUTTON_MIDDLE):
            selection: node_toy.NodeToy | None = self.select_node((pyxel.mouse_x, pyxel.mouse_y))
            if selection is None:
                self.add_continuing((pyxel.mouse_x, pyxel.mouse_y))
                self.sound_node_creation.play()

            else:
                self.remove(selection.get_name())
                self.sound_node_removal.play()

    def update(self) -> None:
        """
        Update positions, nodes, mouse.
        """
        self.node_selection()
        self.arcs_tool()
        self.node_creation()
        
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
            node.draw(self.show_weights)
    
    def display_register(self) -> str:
        """
        Get a formatted string of the `_register`.
        """
        return "GraphToy._register: \n" + ", \n".join([f"{name}: {node.display('  ')}" for name, node in self._register.items()])
        
    def display_adjacency(self) -> str:
        """
        Get a formatted string of the adjacency matrix.
        """
        matrix: list[list[float]] = list()
        heads: list[node_toy.NodeToy] = [node for node in self._register.values()]
        columns_size: list[int] = [0 for _ in range(len(heads))]
        column_separator: str = "│"

        for head in heads:
            adjacency: list[float] = list()
            for index in range(len(heads)):
                if heads[index] in head.get_next():
                    adjacency.append(head.get_next()[heads[index]])
                else:
                    adjacency.append(0)
            matrix.append(adjacency)

        # Get sizes.
        for index in range(len(heads)):
            head = str(heads[index].get_name())
            if len(head) > columns_size[index]:
                columns_size[index] = len(head)

        for index_row in range(len(matrix)):
            for index_column in range(len(matrix[index_row])):
                weight: str = str(matrix[index_row][index_column])
                if len(weight) > columns_size[index_column]:
                    columns_size[index_column] = len(weight)

        total_length: int = 3
        row_separator: str = "\n─┼"
        for size in columns_size:
            total_length += size + 1
            row_separator += "─" * size + "┼"

        row_separator += "\n"

        # Format.
        table: list[str] = [" " + column_separator + column_separator.join([
            graphics.justify(heads[index_column].get_name(), columns_size[index_column]) 
            for index_column in range(len(heads))
        ])]

        for index_row in range(len(matrix)):
            line: str = heads[index_row].get_name() + column_separator
            for index_column in range(len(matrix[index_row])):
                weight: str = str(matrix[index_row][index_column])
                line += graphics.justify(weight, columns_size[index_column]) + column_separator
            
            table.append(line)

        return row_separator.join(table)

    def display_dict(self, tab: str = "  ") -> str:
        """
        Get the dictionary of neighbors.
        """
        lines: list[str] = ["{"]
        for name, node in self._register.items():
            following: list[str] = [
                f"{node.get_name()}: {weight}" 
                for node, weight in node.get_next().items()
            ]
            lines.append(f"{tab}{name}: \x7b{', '.join(following)}\x7d")
        
        return ", \n".join(lines)
