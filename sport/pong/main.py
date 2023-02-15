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
from sport.pong.config import FPS, PADDLE_LEFT_RECT, PADDLE_SPEED, GAME_LIMITS


class Game(World):

    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        window = Window(config.WINDOW_SIZE)
        self.create_entity(window)

        # Left Paddle Entity
        lp_rectangle = Rectangle(*PADDLE_LEFT_RECT)
        lp_collision_rectangle = Collision()
        lp_limit = LimitPosition(*GAME_LIMITS)
        lp_surface = pygame.Surface(PADDLE_LEFT_RECT[2:4])
        lp_surface.fill(pygame.Color("white"))
        lp_sprite = Sprite(lp_surface, PADDLE_LEFT_RECT[0:2])
        lp_follow_rectangle = SpriteFollowRectangle()

        lp_entity = self.create_entity(
            lp_rectangle, lp_collision_rectangle, lp_limit, lp_sprite, lp_follow_rectangle
        )

        self.add_component(
            lp_entity,
            KeyboardInput(
                {
                    pygame.K_UP: self.move_paddle_up,
                    pygame.K_DOWN: self.move_paddle_down,
                },
                is_repeated=True
            )
        )

        self.add_processor(Renderer(FPS))
        self.add_processor(Updater())
        self.add_processor(RectangleMover())
        self.add_processor(RectangleCollider())
        self.add_processor(SpriteMover())
        self.add_processor(LimitPositionChecker())
        self.add_processor(BackToLimitMover())

    def move_paddle_up(self, ent: int, world: World):
        world.publish(MoveRectangle(ent, 0, - world.process_dt * PADDLE_SPEED))

    def move_paddle_down(self, ent: int, world: World):
        world.publish(MoveRectangle(ent, 0, + world.process_dt * PADDLE_SPEED))


if __name__ == '__main__':
    Game().run()
