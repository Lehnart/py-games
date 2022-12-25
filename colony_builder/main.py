from colony_builder import config, cursor

from colony_builder.engine.components.window import Window
from colony_builder.engine.mesper import World
from colony_builder.engine.processors.renderer import Renderer
from colony_builder.engine.processors.sprite_mover import SpriteMover
from colony_builder.engine.processors.updater import Updater


class Game(World):

    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        window = Window(config.WINDOW_SIZE)
        self.create_entity(window)

        for entity in config.GROUND_ENTITIES:
            self.create_entity(entity)

        self.create_entity(config.CASTLE_ENTITY)
        self.create_entity(cursor.SPRITE, cursor.KEYBOARD_INPUT)

        self.add_processor(Renderer(60))
        self.add_processor(Updater())
        self.add_processor(SpriteMover())


if __name__ == '__main__':
    game_world = Game()
    while game_world.is_running:
        game_world.process()
