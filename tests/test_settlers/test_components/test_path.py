from colony_builder.engine.components.grid_position import GridPosition
from colony_builder.engine.mesper import World
from colony_builder.settlers.components.flag import Flag
from colony_builder.settlers.components.path import Path
from colony_builder.settlers.components.road import Road


class TestPath:

    @staticmethod
    def create_test_path(world: World) -> int:
        flag1 = world.create_entity(Flag(), GridPosition(0, 0))
        flag2 = world.create_entity(Flag(), GridPosition(2, 0))
        road1 = world.create_entity(Road(), GridPosition(0, 0))
        road2 = world.create_entity(Road(), GridPosition(1, 0))
        road3 = world.create_entity(Road(), GridPosition(2, 0))
        path_ent = world.create_entity(Path(flag1, flag2, [road1, road2, road3]))
        return path_ent
