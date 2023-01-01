from typing import Tuple

from colony_builder.engine.components.grid_position import GridPosition
from colony_builder.engine.mesper import Processor
from colony_builder.settlers.components.hauler import Hauler
from colony_builder.settlers.components.path import Path
from colony_builder.settlers.events.move_agent import MoveAgent


class HaulerUpdater(Processor):

    def compute_path_mean_position(self, path_comp: Path) -> Tuple[float, float]:
        road_ents = path_comp.road_ents
        grid_pos_comps = [self.world.component_for_entity(road_ent, GridPosition) for road_ent in road_ents]
        gpxs, gpys = [gpc.pos[0] + 0.5 for gpc in grid_pos_comps], [gpc.pos[1] + 0.5 for gpc in grid_pos_comps]
        return sum(gpxs) / len(gpxs), sum(gpys) / len(gpys)

    def process(self):
        haulers = self.world.get_component(Hauler)
        for hauler_ent, hauler_comp in haulers:
            path_comp = self.world.component_for_entity(hauler_comp.path_ent, Path)
            mean_pos = self.compute_path_mean_position(path_comp)
            self.world.publish(MoveAgent(hauler_ent, mean_pos))
