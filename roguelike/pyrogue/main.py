from mesper.components.window import Window
from mesper.mesper import World
from mesper.processors.renderer import Renderer
from mesper.processors.updater import Updater
from roguelike.pyrogue import config


class Game(World):

    def __init__(self):
        super().__init__()
        self._is_running: bool = True


        window = Window(config.WINDOW_SIZE)
        self.create_entity(window)

        self.add_processor(Renderer(60))
        self.add_processor(Updater())


if __name__ == '__main__':
    game_world = Game()
    while game_world.is_running:
        game_world.process()
