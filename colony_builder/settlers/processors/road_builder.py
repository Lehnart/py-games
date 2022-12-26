from typing import Tuple

from colony_builder.engine.components.grid_position import GridPosition
from colony_builder.engine.components.sprite import Sprite
from colony_builder.engine.mesper import Processor
from colony_builder.settlers import config
from colony_builder.settlers.components.flag import Flag
from colony_builder.settlers.components.path import Path
from colony_builder.settlers.components.road import Road
from colony_builder.settlers.config import FLAG_SURFACE
from colony_builder.settlers.events.put_flag import PutFlag


class RoadBuilder(Processor):

    def __init__(self):
        self.is_first_flag_set = False
        self.flag1_ent = None

    def create_road(self, road_x: int, road_y: int):
        return self.world.create_entity(
            Sprite(
                config.ROAD_SURFACE,
                (road_x * config.SPRITE_SIZE, road_y * config.SPRITE_SIZE),
                config.ROAD_LAYER
            ),
            GridPosition(road_x, road_y),
            Road()
        )

    def create_flag(self, flag_x: int, flag_y: int, sprite_x, sprite_y) -> int:
        return self.world.create_entity(
            Sprite(FLAG_SURFACE, (sprite_x, sprite_y), config.BUILDING_LAYER),
            GridPosition(flag_x, flag_y),
            Flag()
        )

    def set_first_flag(self, grid_x: int, grid_y: int, sprite_x: int, sprite_y: int):
        self.flag1_ent = self.create_flag(grid_x, grid_y, sprite_x, sprite_y)
        self.is_first_flag_set = True

    def create_roads(self, flag1_pos: Tuple[int, int], flag2_pos: Tuple[int, int]):
        road_ents = []
        flag1_x, flag1_y = flag1_pos
        flag2_x, flag2_y = flag2_pos
        for road_x in range(min(flag1_x, flag2_x), max(flag1_x, flag2_x) + 1):
            for road_y in range(min(flag1_y, flag2_y), max(flag1_y, flag2_y) + 1):
                road_ents.append(self.create_road(road_x, road_y))
        return road_ents

    def process(self):

        put_flag_events = self.world.receive(PutFlag)
        for put_flag_event in put_flag_events:
            grid_x, grid_y = put_flag_event.grid_position
            sprite_x, sprite_y = grid_x * config.SPRITE_SIZE, grid_y * config.SPRITE_SIZE

            if not self.is_first_flag_set:
                self.set_first_flag(grid_x, grid_y, sprite_x, sprite_y)

            else:
                first_flag_position_comp = self.world.component_for_entity(self.flag1_ent, GridPosition)
                flag1_x, flag1_y = first_flag_position_comp.pos
                flag1_ent = self.flag1_ent
                road_ents = []

                if flag1_x != grid_x and flag1_y != grid_y:
                    self.world.delete_entity(self.flag1_ent)

                else:
                    flag2_x, flag2_y = grid_x, grid_y
                    flag2_ent = self.create_flag(grid_x, grid_y, sprite_x, sprite_y)
                    road_ents = self.create_roads((flag1_x, flag1_y), (flag2_x, flag2_y))

                    self.world.create_entity(
                        Path(flag1_ent, flag2_ent, road_ents)
                    )

                self.is_first_flag_set = False
                self.flag1_ent = None
