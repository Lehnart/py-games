import datetime
import time

import pygame

from colony_builder.engine.components.sprite import Sprite
from colony_builder.engine.components.window import Window
from colony_builder.engine.mesper import World
from colony_builder.engine.processors.renderer import Renderer


class TestRenderer:

    def test_constructor(self):
        renderer = Renderer(30)
        assert renderer.frame_per_seconds == 30

    def test_process(self):
        world = World()
        fps = 10
        renderer = Renderer(fps)
        construction_date = datetime.datetime.now()

        world.add_processor(renderer)
        world.process()
        assert len(renderer.last_time_drawn_dict.items()) == 0

        entity = world.create_entity(Window((640, 480)))
        world.process()
        assert len(renderer.last_time_drawn_dict.items()) == 1
        ent, last_drawn_time = list(renderer.last_time_drawn_dict.items())[0]
        assert ent == entity
        assert construction_date < last_drawn_time

        world.process()
        assert len(renderer.last_time_drawn_dict.items()) == 1
        ent, next_last_drawn_time = list(renderer.last_time_drawn_dict.items())[0]
        assert ent == entity
        assert last_drawn_time == next_last_drawn_time

        time.sleep(0.11)
        world.process()
        assert len(renderer.last_time_drawn_dict.items()) == 1
        ent, next_last_drawn_time = list(renderer.last_time_drawn_dict.items())[0]
        assert ent == entity
        assert next_last_drawn_time >= last_drawn_time + datetime.timedelta(seconds=(1. / fps))

    def test_sort_sprites(self):
        pygame.init()
        surf = pygame.Surface((5, 5))

        comp1 = Sprite(surf, (1, 1), 1)
        comp2 = Sprite(surf, (2, 2), 2)
        comp3 = Sprite(surf, (3, 3), 3)

        sprites = [comp3, comp2, comp1]
        Renderer.sort_sprites(sprites)
        assert sprites[0].layer < sprites[1].layer < sprites[2].layer
