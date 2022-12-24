import pygame.image

from colony_builder.engine.components.keyboard_input import KeyboardInput
from colony_builder.engine.components.sprite import Sprite
from colony_builder.engine.events.move_sprite import MoveSprite

WINDOW_SIZE = (640, 480)

SPRITE_SIZE = 16

GRASS_SURFACE = pygame.image.load("res/grass.png")
CASTLE_SURFACE = pygame.image.load("res/castle.png")
CURSOR_SURFACE = pygame.image.load("res/cursor.png")
FLAG_SURFACE = pygame.image.load("res/flag.png")

GROUND_ENTITIES = [
    Sprite(GRASS_SURFACE, (x, y), 0)
    for y in range(0, WINDOW_SIZE[1], SPRITE_SIZE)
    for x in range(0, WINDOW_SIZE[0], SPRITE_SIZE)
]
CASTLE_ENTITY = Sprite(CASTLE_SURFACE, (640 // 16 * 8, 480 // 16 * 8), 1)

CURSOR_SPRITE = Sprite(CURSOR_SURFACE, (640 // 16 * 8, 480 // 16 * 8), 2)
CURSOR_KEYBOARD_INPUT = KeyboardInput(
    {
        pygame.K_z: lambda ent, world : world.publish(MoveSprite(ent, (0, -16))),
        pygame.K_d: lambda ent, world : world.publish(MoveSprite(ent, (16, 0))),
        pygame.K_s: lambda ent, world : world.publish(MoveSprite(ent, (0, 16))),
        pygame.K_q: lambda ent, world : world.publish(MoveSprite(ent, (-16, 0))),
    }
)
