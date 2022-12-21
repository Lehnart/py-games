from typing import Tuple

import pygame

from mesper import Component


class Window(Component):

    def __init__(self, size: Tuple[int, int]):
        pygame.init()
        self._window_surface: pygame.Surface = pygame.display.set_mode(size)

    def surface(self) -> pygame.Surface:
        return self._window_surface
