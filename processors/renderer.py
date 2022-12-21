import datetime

import pygame

from components.window import Window
from mesper import Processor


class Renderer(Processor):

    def __init__(self, frame_per_seconds: float):
        super().__init__()
        self.frame_per_seconds = frame_per_seconds
        self.last_time_drawn = datetime.datetime.now()

    def process(self):

        if datetime.datetime.now() - self.last_time_drawn < datetime.timedelta(seconds=1. / self.frame_per_seconds):
            return
        self.last_time_drawn = datetime.datetime.now()

        for _, [window_component] in self.world.get_components(Window):
            self._draw_on_window(window_component)

    @staticmethod
    def _draw_on_window(window_component: Window):

        window_surface = window_component.surface()
        pygame.display.flip()
        window_surface.fill((0, 0, 0))
