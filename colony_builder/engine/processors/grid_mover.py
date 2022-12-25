from colony_builder.engine.components.grid_position import GridPosition
from colony_builder.engine.events.move_on_grid import MoveOnGrid
from colony_builder.engine.mesper import Processor


class GridMover(Processor):

    def process(self):
        move_events = self.world.receive(MoveOnGrid)

        for move_event in move_events:
            grid_position_component = self.world.component_for_entity(move_event.ent, GridPosition)
            grid_position_component.move(*move_event.movement)
