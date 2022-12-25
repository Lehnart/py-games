from colony_builder.engine.components.grid_position import GridPosition
from colony_builder.engine.components.sprite import Sprite
from colony_builder.engine.mesper import Processor
from colony_builder.settlers.config import FLAG_SURFACE
from colony_builder.settlers.events.put_flag import PutFlag


class RoadBuilder(Processor):

    def __init__(self):
        self.is_first_flag_set = False
        self.first_flag_ent = None

    def process(self):

        put_flag_events = self.world.receive(PutFlag)
        for put_flag_event in put_flag_events:
            grid_x, grid_y = put_flag_event.grid_position
            sprite_x, sprite_y = grid_x * 16, grid_y * 16

            if not self.is_first_flag_set:

                self.first_flag_ent = self.world.create_entity(
                    Sprite(FLAG_SURFACE, (sprite_x, sprite_y), 1),
                    GridPosition(grid_x, grid_y)
                )
                self.is_first_flag_set = True

            else:
                first_flag_position_comp = self.world.component_for_entity(self.first_flag_ent, GridPosition)
                first_flag_grid_x, first_flag_grid_y = first_flag_position_comp.pos

                if first_flag_grid_x != grid_x and first_flag_grid_y != grid_y:
                    self.world.delete_entity(self.first_flag_ent)

                else:
                    self.world.create_entity(
                        Sprite(FLAG_SURFACE, (sprite_x, sprite_y), 1),
                        GridPosition(grid_x, grid_y)
                    )

                self.is_first_flag_set = False
                self.first_flag_ent = None
