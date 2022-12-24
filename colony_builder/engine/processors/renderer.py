import datetime

import pygame

from colony_builder.engine.components.sprite import Sprite
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

    def _draw_on_window(self, window_component: Window):

        sprites = [c[1] for c in self.world.get_component(Sprite)]
        sprites.sort(key=lambda s: s.layer)

        window_surface = window_component.surface()
        window_surface.fill((0, 0, 0))

        for sprite in sprites:
            window_surface.blit(sprite.surface, sprite.top_left_position)

        pygame.display.flip()
