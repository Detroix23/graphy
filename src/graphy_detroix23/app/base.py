"""
# Graphy.
/src/graphy_detroix23/app/base.py
"""

import pyxel

from graphy_detroix23.modules import defaults
from graphy_detroix23.app import graph_toy, mouse, buttons
 
class App:
    """
    # Main `App`.
    Encloses the full application state and window.
    """
    graph: graph_toy.GraphToy
    mouse_handler: mouse.Mouse
    background_color: int
    widgets: list[buttons.Button]

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
        self.background_color = pyxel.COLOR_BLACK
        self.widgets = self.load_widgets()

        pyxel.init(
            width,
            height,
            title="Graphy",
            fps=fps,
            quit_key=pyxel.KEY_ESCAPE,
        )

        pyxel.load(str(defaults.RESOURCE_FILE))

        self.first()

    def load_widgets(self) -> list[buttons.Button]:
        """
        Initialize the buttons
        """
        return [
            buttons.Button(
                (10.0, 10.0),
                (140.0, 30.0),
                ["Print dict"],
                lambda _: print(f"\nDictionary:\n{self.graph.display_register()}"),
                color=pyxel.COLOR_GRAY,
                color_clicked=pyxel.COLOR_WHITE,
                font=defaults.FONT_BIG_BLUE,
                margin=(10.0, 10.0),
            ),
            buttons.Button(
                (10.0, 45.0),
                (140.0, 30.0),
                ["Print adjacency"],
                lambda _: print(f"\nAdjacency matrix:\n{self.graph.display_adjacency()}"),
                color=pyxel.COLOR_GRAY,
                color_clicked=pyxel.COLOR_WHITE,
                font=defaults.FONT_BIG_BLUE,
                margin=(10.0, 10.0),
            )
        ]
 
    def first(self) -> None:
        """
        First actions, taken 1 time only, just before the start of the game loop.
        """
        self.graph.add("A")
        self.graph.add("B")
        for _ in range(10):
            self.graph.add_continuing()
        
        self.graph["A"].batch_next((
            (self.graph["B"], 1.0),
            (self.graph["C"], 1.0)
        ))

        self.graph.default_position(100.0 + self.graph.card)

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

        for widget in self.widgets:
            widget.update()

    def draw(self) -> None:
        """
        Application general periodic drawing, in the game loop. 
        """
        pyxel.cls(self.background_color)

        self.graph.draw()

        for widget in self.widgets:
            widget.draw()

        self.mouse_handler.draw()


def main() -> None:
    """
    Default launch.
    """
    app = App(
        width=700, 
        height=500, 
        fps=30,
    )
    
    app.run()
