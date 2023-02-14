from mesper.components.rectangle import Rectangle
from mesper.components.window import Window
from mesper.mesper import World
from mesper.processors.renderer import Renderer
from mesper.processors.updater import Updater
from sport.pong import config
from sport.pong.config import FPS, PADDLE_LEFT_RECT


class Game(World):

    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        window = Window(config.WINDOW_SIZE)
        self.create_entity(window)

        # Left Paddle Entity
        lp_rectangle = Rectangle(*PADDLE_LEFT_RECT)
        self.create_entity(lp_rectangle)

        self.add_processor(Renderer(FPS))
        self.add_processor(Updater())


if __name__ == '__main__':
    Game().run()
