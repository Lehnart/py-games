import datetime

import pygame

from colony_builder.engine.components.window import Window
from colony_builder.engine.mesper import Processor


class Renderer(Processor):

    def __init__(self, frame_per_seconds: float):
        super().__init__()
        self.frame_per_seconds = frame_per_seconds
        self.last_time_drawn_dict = {}

    def process(self):

        for ent, [window_component] in self.world.get_components(Window):
            if ent not in self.last_time_drawn_dict:
                self.last_time_drawn_dict[ent] = datetime.datetime.now()
                self._draw_on_window(window_component)

            else:
                last_time_drawn = self.last_time_drawn_dict[ent]
                if datetime.datetime.now() - last_time_drawn > datetime.timedelta(seconds=1. / self.frame_per_seconds):
                    self.last_time_drawn_dict[ent] = datetime.datetime.now()
                    self._draw_on_window(window_component)

    @staticmethod
    def _draw_on_window(window_component: Window):

        window_surface = window_component.surface()
        pygame.display.flip()
        window_surface.fill((0, 0, 0))
