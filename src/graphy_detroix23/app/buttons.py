"""
# Graphy.
/src/graphy_detroix23/app/buttons.py
"""

import math
from typing import Callable, Self

import pyxel

from graphy_detroix23.modules import sound

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
    sound: sound.MML | None
    font: pyxel.Font | None
    margin: tuple[float, float]
    # Duration in frames.
    _click_time: int
    _click_effect_duration: int

    def __init__(
        self,
        position: tuple[float, float],
        size: tuple[float, float],
        text: list[str],
        action: Callable[[Self], None],
        color: int,
        color_clicked: int = pyxel.COLOR_WHITE,
        sound: sound.MML | None = None,
        font: pyxel.Font | None = None,
        margin: tuple[float, float] = (0.0, 0.0)
    ) -> None:
        """
        Create a `Button`.

        Arguments:
        - `sound`: `str`, MML string.
        """
        self.position = position
        self.size = size
        self.text = text
        self.action = action
        self.color = color
        self.color_clicked = color_clicked
        self.sound = sound
        self.font = font      
        self.margin = margin
        self._click_time = 0
        self._click_effect_duration = 6

    def draw(self) -> None:
        """
        Draw the button to the screen.
        """
        scale: float = 4.0 * math.log(self._click_time + 1)

        if 2 * self._click_time > 0:
            pyxel.dither(min((self._click_time + 1) / self._click_effect_duration, 1.0))
            pyxel.rect(
                self.position[0] - scale,
                self.position[1] - scale,
                self.size[0] + 2 * scale,
                self.size[1] + 2 * scale,
                self.color_clicked,
            )
            pyxel.dither(1.0)

        pyxel.rectb(
            self.position[0] - scale,
            self.position[1] - scale,
            self.size[0] + 2 * scale,
            self.size[1] + 2 * scale,
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
                self._click_time = self._click_effect_duration
                
                if self.sound is not None:
                    self.sound.play()

        if self._click_time > 0:
            self._click_time -= 1