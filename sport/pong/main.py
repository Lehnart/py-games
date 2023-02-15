from typing import Tuple

import pygame

from mesper.components.collision import Collision
from mesper.components.keyboard_input import KeyboardInput
from mesper.components.limit_position import LimitPosition
from mesper.components.rectangle import Rectangle
from mesper.components.sprite import Sprite
from mesper.components.sprite_follow_rectangle import SpriteFollowRectangle
from mesper.components.window import Window
from mesper.events.move_rectangle import MoveRectangle
from mesper.mesper import World
from mesper.processors.limit_position_checker import LimitPositionChecker
from mesper.processors.back_to_limit_mover import BackToLimitMover
from mesper.processors.rectangle_collider import RectangleCollider
from mesper.processors.rectangle_mover import RectangleMover
from mesper.processors.renderer import Renderer
from mesper.processors.sprite_mover import SpriteMover
from mesper.processors.updater import Updater
from sport.pong import config
from sport.pong.config import FPS, PADDLE_LEFT_RECT, PADDLE_SPEED, GAME_LIMITS, PADDLE_RIGHT_RECT, PADDLE_LEFT_INPUT, \
    PADDLE_RIGHT_INPUT


class Game(World):

    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        window = Window(config.WINDOW_SIZE)
        self.create_entity(window)

        # Paddle Entities
        self.create_paddle(PADDLE_LEFT_RECT, PADDLE_LEFT_INPUT)
        self.create_paddle(PADDLE_RIGHT_RECT, PADDLE_RIGHT_INPUT)

        self.add_processor(Renderer(FPS))
        self.add_processor(Updater())
        self.add_processor(RectangleMover())
        self.add_processor(RectangleCollider())
        self.add_processor(SpriteMover())
        self.add_processor(LimitPositionChecker())
        self.add_processor(BackToLimitMover())

    def create_paddle(self, paddle_rect: Tuple[int, int, int, int], inputs: Tuple[int,int]):
        paddle_rectangle = Rectangle(*paddle_rect)
        paddle_collision_rectangle = Collision()
        paddle_limit = LimitPosition(*GAME_LIMITS)
        paddle_surface = pygame.Surface(paddle_rect[2:4])
        paddle_surface.fill(pygame.Color("white"))
        paddle_sprite = Sprite(paddle_surface, paddle_rect[0:2])
        paddle_follow_rectangle = SpriteFollowRectangle()
        paddle_entity = self.create_entity(
            paddle_rectangle, paddle_collision_rectangle, paddle_limit, paddle_sprite, paddle_follow_rectangle
        )
        self.add_component(
            paddle_entity,
            KeyboardInput(
                {
                    inputs[0]: self.move_paddle_up,
                    inputs[1]: self.move_paddle_down,
                },
                is_repeated=True
            )
        )
        return paddle_entity

    @staticmethod
    def move_paddle_up(ent: int, world: World):
        world.publish(MoveRectangle(ent, 0, - world.process_dt * PADDLE_SPEED))

    @staticmethod
    def move_paddle_down(ent: int, world: World):
        world.publish(MoveRectangle(ent, 0, + world.process_dt * PADDLE_SPEED))


if __name__ == '__main__':
    Game().run()
