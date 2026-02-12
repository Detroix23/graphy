"""
# Graphy.
/src/graphy_detroix23/app/base.py
"""

import pyxel

class App:
    """
    # Main `App`.
    Encloses the full application state and window.
    """

    def __init__(
        self,
        width: int,
        height: int,
        fps: int
    ) -> None:
        """
        Initialize the application and default settings.
        """

        pyxel.init(
            width,
            height,
            title="Graphy",
            fps=fps,
            quit_key=pyxel.KEY_ESCAPE,
        )


    def run(self) -> None:
        """
        Starts, runs the application.
        """

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """
        Application general periodic updating, in the game loop. 
        """


    def draw(self) -> None:
        """
        Application general periodic drawing, in the game loop. 
        """