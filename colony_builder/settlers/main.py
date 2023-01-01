from colony_builder.engine.components.sprite import Sprite
from colony_builder.engine.components.window import Window
from colony_builder.engine.mesper import World
from colony_builder.engine.processors.grid_mover import GridMover
from colony_builder.engine.processors.renderer import Renderer
from colony_builder.engine.processors.sprite_mover import SpriteMover
from colony_builder.engine.processors.updater import Updater
from colony_builder.settlers import config, cursor
from colony_builder.settlers.components.agent import Agent
from colony_builder.settlers.processors.agent_mover import AgentMover
from colony_builder.settlers.processors.hauler_updater import HaulerUpdater
from colony_builder.settlers.processors.job_giver import JobGiver
from colony_builder.settlers.processors.path_assigner import PathAssigner
from colony_builder.settlers.processors.road_builder import RoadBuilder


class Game(World):

    def __init__(self):
        super().__init__()
        self._is_running: bool = True

        window = Window(config.WINDOW_SIZE)
        self.create_entity(window)

        for entity in config.GROUND_ENTITIES:
            self.create_entity(entity)

        self.create_entity(config.CASTLE_ENTITY)
        self.create_entity(cursor.SPRITE, cursor.KEYBOARD_INPUT, cursor.GRID_POSITION)

        for pos_x in range(0, 5):
            for pos_y in range(0, 5):
                self.create_entity(
                    Sprite(config.HUMAN_SURFACE, (pos_x * 16, pos_y * 16), config.AGENT_LAYER),
                    Agent((pos_x, pos_y), 5.)
                )

        self.add_processor(Renderer(60))
        self.add_processor(Updater())
        self.add_processor(SpriteMover())
        self.add_processor(GridMover())
        self.add_processor(RoadBuilder())
        self.add_processor(PathAssigner())
        self.add_processor(AgentMover())
        self.add_processor(JobGiver())
        self.add_processor(HaulerUpdater())


if __name__ == '__main__':
    game_world = Game()
    while game_world.is_running:
        game_world.process()
