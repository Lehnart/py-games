from typing import Tuple

import pygame

from colony_builder.engine.mesper import Component


class Sprite(Component):

    def __init__(self, surface: pygame.Surface, top_left_position: Tuple[int, int], layer: int = 0):
        self.surface = surface
        self.top_left_position = top_left_position
        self.layer = layer
