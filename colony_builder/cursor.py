import pygame

from colony_builder.config import FLAG_SURFACE
from colony_builder.engine.components.keyboard_input import KeyboardInput
from colony_builder.engine.components.sprite import Sprite
from colony_builder.engine.events.move_sprite import MoveSprite
from colony_builder.engine.mesper import World

SURFACE = pygame.image.load("res/cursor.png")


def create_flag(ent: int, world: World):
    cursor_sprite_comp = world.component_for_entity(ent, Sprite)
    if cursor_sprite_comp is None:
        return
    world.create_entity(Sprite(FLAG_SURFACE, cursor_sprite_comp.top_left_position, 1))


SPRITE = Sprite(SURFACE, (640 // 16 * 8, 480 // 16 * 8), 2)
KEYBOARD_INPUT = KeyboardInput(
    {
        pygame.K_z: lambda ent, world: world.publish(MoveSprite(ent, (0, -16))),
        pygame.K_UP: lambda ent, world: world.publish(MoveSprite(ent, (0, -16))),

        pygame.K_d: lambda ent, world: world.publish(MoveSprite(ent, (16, 0))),
        pygame.K_RIGHT: lambda ent, world: world.publish(MoveSprite(ent, (16, 0))),

        pygame.K_s: lambda ent, world: world.publish(MoveSprite(ent, (0, 16))),
        pygame.K_DOWN: lambda ent, world: world.publish(MoveSprite(ent, (0, 16))),

        pygame.K_q: lambda ent, world: world.publish(MoveSprite(ent, (-16, 0))),
        pygame.K_LEFT: lambda ent, world: world.publish(MoveSprite(ent, (-16, 0))),

        pygame.K_SPACE: create_flag
    }
)
