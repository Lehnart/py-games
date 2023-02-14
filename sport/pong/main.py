import pygame

from mesper.components.keyboard_input import KeyboardInput
from mesper.components.rectangle import Rectangle
from mesper.components.window import Window
from mesper.events.move_rectangle import MoveRectangle
from mesper.mesper import World
from mesper.processors.rectangle_mover import RectangleMover
from mesper.processors.renderer import Renderer
from mesper.processors.updater import Updater
from sport.pong import config
from sport.pong.config import FPS, PADDLE_LEFT_RECT, PADDLE_SPEED


class Game(World):

    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        window = Window(config.WINDOW_SIZE)
        self.create_entity(window)

        # Left Paddle Entity
        lp_rectangle = Rectangle(*PADDLE_LEFT_RECT)
        lp_entity = self.create_entity(lp_rectangle)
        self.add_component(
            lp_entity,
            KeyboardInput(
                {
                    pygame.K_UP:
                        lambda ent, world: world.publish(MoveRectangle(ent, 0, - world.process_dt * PADDLE_SPEED)),
                    pygame.K_DOWN:
                        lambda ent, world: world.publish(MoveRectangle(ent, 0, + world.process_dt * PADDLE_SPEED)),
                }
            )
        )

        self.add_processor(Renderer(FPS))
        self.add_processor(Updater())
        self.add_processor(RectangleMover())


if __name__ == '__main__':
    Game().run()
