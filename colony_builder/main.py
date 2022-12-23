from colony_builder.engine.components.window import Window
from colony_builder.engine.mesper import World
from colony_builder.engine.processors.renderer import Renderer
from colony_builder.engine.processors.updater import Updater

WINDOW_SIZE = (640, 480)


class Game(World):

    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        # Window entity
        window = Window(WINDOW_SIZE)
        self.create_entity(window)

        self.add_processor(Renderer(60))
        self.add_processor(Updater())


if __name__ == '__main__':
    game_world = Game()
    while game_world.is_running:
        game_world.process()
