import pygame

from colony_builder.engine.components.grid_position import GridPosition
from colony_builder.engine.components.keyboard_input import KeyboardInput
from colony_builder.engine.components.sprite import Sprite
from colony_builder.engine.events.move_on_grid import MoveOnGrid
from colony_builder.engine.events.move_sprite import MoveSprite
from colony_builder.engine.mesper import World
from colony_builder.settlers.events.put_flag import PutFlag

SURFACE = pygame.image.load("res/cursor.png")

CURSOR_LAYER = 3

def put_flag(ent: int, world: World):
    position = world.component_for_entity(ent, GridPosition)
    world.publish(PutFlag(position.pos))


def move_up(ent: int, world: World):
    world.publish(MoveSprite(ent, (0, -16)))
    world.publish(MoveOnGrid(ent, (0, -1)))


def move_right(ent: int, world: World):
    world.publish(MoveSprite(ent, (16, 0)))
    world.publish(MoveOnGrid(ent, (1, 0)))


def move_down(ent: int, world: World):
    world.publish(MoveSprite(ent, (0, 16)))
    world.publish(MoveOnGrid(ent, (0, 1)))


def move_left(ent: int, world: World):
    world.publish(MoveSprite(ent, (-16, 0)))
    world.publish(MoveOnGrid(ent, (-1, 0)))


SPRITE = Sprite(SURFACE, (640 // 16 * 8, 480 // 16 * 8), CURSOR_LAYER)
GRID_POSITION = GridPosition(640 // 16 * 8 // 16, 480 // 16 * 8 // 16)
KEYBOARD_INPUT = KeyboardInput(
    {
        pygame.K_z: move_up,
        pygame.K_UP: move_up,

        pygame.K_d: move_right,
        pygame.K_RIGHT: move_right,

        pygame.K_s: move_down,
        pygame.K_DOWN: move_down,

        pygame.K_q: move_left,
        pygame.K_LEFT: move_left,

        pygame.K_SPACE: put_flag
    }
)
