import pygame

from colony_builder.engine.components.sprite import Sprite
from colony_builder.engine.events.move_sprite import MoveSprite
from colony_builder.engine.mesper import World
from colony_builder.engine.processors.sprite_mover import SpriteMover


class TestSpriteMover:

    def test_process(self):
        world = World()

        surf = pygame.Surface((5, 5))
        ent = world.create_entity(Sprite(surf, (10, 10)))

        world.add_processor(SpriteMover())

        world.publish(MoveSprite(ent, (-3, 7)))
        world.process()

        sprite_comp = world.component_for_entity(ent, Sprite)
        assert sprite_comp.top_left_position == (7, 17)
