from typing import Tuple

import pygame

from mesper.components.bounce import Bounce
from mesper.components.collision import Collision
from mesper.components.keyboard_input import KeyboardInput
from mesper.components.limit_position import LimitPosition
from mesper.components.rectangle import Rectangle
from mesper.components.speed import Speed
from mesper.components.sprite import Sprite
from mesper.components.window import Window
from mesper.events.move_rectangle import MoveRectangle
from mesper.mesper import World
from mesper.processors.bouncer import Bouncer
from mesper.processors.limit_position_checker import LimitPositionChecker
from mesper.processors.back_to_limit_mover import BackToLimitMover
from mesper.processors.rectangle_collider import RectangleCollider
from mesper.processors.rectangle_mover import RectangleMover
from mesper.processors.renderer import Renderer
from mesper.processors.sprite_mover import SpriteMover
from mesper.processors.keyboard_updater import KeyboardUpdater
from sport.pong import config
from sport.pong.config import FPS, PADDLE_LEFT_RECT, PADDLE_SPEED, GAME_LIMITS, PADDLE_RIGHT_RECT, PADDLE_LEFT_INPUT, \
    PADDLE_RIGHT_INPUT, CENTER_LINE_SPRITE, BALL_RECT, BALL_SPEED


class Game(World):

    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        window = Window(config.WINDOW_SIZE)
        self.create_entity(window)

        # Paddle Entities
        self.create_paddle(PADDLE_LEFT_RECT, PADDLE_LEFT_INPUT)
        self.create_paddle(PADDLE_RIGHT_RECT, PADDLE_RIGHT_INPUT)

        # center line
        self.create_entity(Sprite(CENTER_LINE_SPRITE, (GAME_LIMITS[1]//2, 0)))

        # ball
        self.create_ball()

        self.add_processor(Renderer(FPS))
        self.add_processor(KeyboardUpdater())
        self.add_processor(RectangleMover())
        self.add_processor(RectangleCollider())
        self.add_processor(SpriteMover())
        self.add_processor(LimitPositionChecker())
        self.add_processor(BackToLimitMover())
        self.add_processor(Bouncer())

    def create_ball(self):
        rectangle = Rectangle(*BALL_RECT)
        collision = Collision()
        rect_limit = LimitPosition(*GAME_LIMITS)
        ball_surface = pygame.Surface(BALL_RECT[2:4])
        ball_surface.fill(pygame.Color("white"))
        rect_sprite = Sprite(ball_surface)
        speed = Speed(*BALL_SPEED)
        bounce = Bounce(-1., 1.)
        self.create_entity(rectangle, rect_limit, rect_sprite, collision, speed, bounce)

    def create_paddle(self, paddle_rect: Tuple[int, int, int, int], inputs: Tuple[int,int]):
        paddle_rectangle = Rectangle(*paddle_rect)
        paddle_collision_rectangle = Collision()
        paddle_limit = LimitPosition(*GAME_LIMITS)
        paddle_surface = pygame.Surface(paddle_rect[2:4])
        paddle_surface.fill(pygame.Color("white"))
        paddle_sprite = Sprite(paddle_surface, paddle_rect[0:2])
        paddle_entity = self.create_entity(
            paddle_rectangle, paddle_collision_rectangle, paddle_limit, paddle_sprite)
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
