"""
# Graphy.
/src/graphy_detroix23/app/buttons.py
"""

from typing import Callable, Self

import pyxel

class Button:
    """
    # Interactive `Button` class.
    """
    position: tuple[float, float]
    size: tuple[float, float]
    text: list[str]
    action: Callable[[Self], None]
    color: int
    color_clicked: int
    font: pyxel.Font | None
    margin: tuple[float, float]
    _is_clicked: bool

    def __init__(
        self,
        position: tuple[float, float],
        size: tuple[float, float],
        text: list[str],
        action: Callable[[Self], None],
        color: int,
        color_clicked: int = pyxel.COLOR_WHITE,
        font: pyxel.Font | None = None,
        margin: tuple[float, float] = (0.0, 0.0)
    ) -> None:
        self.position = position
        self.size = size
        self.text = text
        self.action = action
        self.color = color
        self.color_clicked = color_clicked
        self.font = font      
        self.margin = margin
        self._is_clicked = False

    def draw(self) -> None:
        """
        Draw the button to the screen.
        """
        if self._is_clicked:
            pyxel.rect(
                self.position[0],
                self.position[1],
                self.size[0],
                self.size[1],
                self.color_clicked,
            )

        pyxel.rectb(
            self.position[0],
            self.position[1],
            self.size[0],
            self.size[1],
            self.color,
        )
        for index in range(len(self.text)):
            pyxel.text(
                self.position[0] + self.margin[0],
                self.position[1] + self.margin[1] + index * 12,
                self.text[index],
                self.color,
                self.font,
            )


    def update(self) -> None:
        """
        Update the button: listen to click and execute the `action`.
        """
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if (
                pyxel.mouse_x > self.position[0] and pyxel.mouse_x < self.position[0] + self.size[0]
                and pyxel.mouse_y > self.position[1] and pyxel.mouse_y < self.position[1] + self.size[1]
            ):
                self.action(self)
                self._is_clicked = True
        
        elif pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            if (
                pyxel.mouse_x > self.position[0] and pyxel.mouse_x < self.position[0] + self.size[0]
                and pyxel.mouse_y > self.position[1] and pyxel.mouse_y < self.position[1] + self.size[1]
            ):
                self._is_clicked = True
        
        else:
            if (
                pyxel.mouse_x > self.position[0] and pyxel.mouse_x < self.position[0] + self.size[0]
                and pyxel.mouse_y > self.position[1] and pyxel.mouse_y < self.position[1] + self.size[1]
            ):
                self._is_clicked = False
    