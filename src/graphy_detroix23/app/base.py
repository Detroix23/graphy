"""
# Graphy.
/src/graphy_detroix23/app/base.py
"""

import pyxel

from graphy_detroix23.modules import defaults
from graphy_detroix23.app import graph_toy, mouse
 
class App:
    """
    # Main `App`.
    Encloses the full application state and window.
    """
    graph: graph_toy.GraphToy
    mouse_handler: mouse.Mouse
    background_color: int

    def __init__(
        self,
        width: int,
        height: int,
        fps: int
    ) -> None:
        """
        Initialize the application and default settings.
        """
        self.graph = graph_toy.GraphToy(self)
        self.mouse_handler = mouse.Mouse(self)
        self.background_color = 0

        pyxel.init(
            width,
            height,
            title="Graphy",
            fps=fps,
            quit_key=pyxel.KEY_ESCAPE,
        )

        pyxel.load(str(defaults.RESOURCE_FILE))

        self.first()

    def first(self) -> None:
        """
        First actions, taken 1 time only, just before the start of the game loop.
        """
        self.graph.add("A")
        self.graph.add("B")
        self.graph.add("C")
        
        self.graph["A"].batch_next((
            (self.graph["B"], 1.0),
            (self.graph["C"], 1.0)
        ))

        print(self.graph.display_register())

    def run(self) -> None:
        """
        Starts, runs the application.
        """
        pyxel.mouse(False)
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """
        Application general periodic updating, in the game loop. 
        """
        self.graph.update()

    def draw(self) -> None:
        """
        Application general periodic drawing, in the game loop. 
        """
        pyxel.cls(self.background_color)

        self.graph.draw()
        self.mouse_handler.draw()

def main() -> None:
    """
    Default launch.
    """
    app = App(700, 500, 30)
    
    app.run()
