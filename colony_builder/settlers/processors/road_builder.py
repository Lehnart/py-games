from colony_builder.engine.components.grid_position import GridPosition
from colony_builder.engine.components.sprite import Sprite
from colony_builder.engine.mesper import Processor
from colony_builder.settlers import config
from colony_builder.settlers.components.flag import Flag
from colony_builder.settlers.components.road import Road
from colony_builder.settlers.config import FLAG_SURFACE
from colony_builder.settlers.events.put_flag import PutFlag


class RoadBuilder(Processor):

    def __init__(self):
        self.is_first_flag_set = False
        self.first_flag_ent = None

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

    def create_flag(self, flag_x: int, flag_y: int, sprite_x, sprite_y):
        return self.world.create_entity(
            Sprite(FLAG_SURFACE, (sprite_x, sprite_y), config.BUILDING_LAYER),
            GridPosition(flag_x, flag_y),
            Flag()
        )

    def process(self):

        put_flag_events = self.world.receive(PutFlag)
        for put_flag_event in put_flag_events:
            grid_x, grid_y = put_flag_event.grid_position
            sprite_x, sprite_y = grid_x * config.SPRITE_SIZE, grid_y * config.SPRITE_SIZE

            if not self.is_first_flag_set:
                self.first_flag_ent = self.create_flag(grid_x, grid_y, sprite_x, sprite_y)
                self.is_first_flag_set = True

            else:
                first_flag_position_comp = self.world.component_for_entity(self.first_flag_ent, GridPosition)
                flag1_x, flag1_y = first_flag_position_comp.pos

                if flag1_x != grid_x and flag1_y != grid_y:
                    self.world.delete_entity(self.first_flag_ent)

                else:
                    flag2_x, flag2_y = grid_x, grid_y
                    self.create_flag(grid_x, grid_y, sprite_x, sprite_y)

                    if flag2_x != flag1_x:
                        road_y = flag1_y
                        for road_x in range(min(flag1_x, flag2_x), max(flag1_x, flag2_x) + 1):
                            self.create_road(road_x, road_y)
                    else:
                        road_x = flag1_x
                        for road_y in range(min(flag1_y, flag2_y), max(flag1_y, flag2_y) + 1):
                            self.create_road(road_x, road_y)

                self.is_first_flag_set = False
                self.first_flag_ent = None
