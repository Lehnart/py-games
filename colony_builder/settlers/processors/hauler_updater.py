import math
from typing import Tuple, Optional

from colony_builder.engine.components.grid_position import GridPosition
from colony_builder.engine.components.sprite import Sprite
from colony_builder.engine.mesper import Processor
from colony_builder.settlers import config
from colony_builder.settlers.components.agent import Agent
from colony_builder.settlers.components.hauler import Hauler
from colony_builder.settlers.components.path import Path
from colony_builder.settlers.components.resource import Resource
from colony_builder.settlers.events.move_agent import MoveAgent


class HaulerUpdater(Processor):

    def __init__(self):
        self.distance_tolerance = 0.001

    def process(self):
        haulers = self.world.get_components(Hauler, Agent)
        for hauler_ent, [hauler_comp, hauler_agent] in haulers:
            path_comp = self.world.component_for_entity(hauler_comp.path_ent, Path)
            mean_pos = self.compute_path_mean_position(path_comp)
            dist = math.sqrt((hauler_agent.pos[0] - mean_pos[0]) ** 2 + (hauler_agent.pos[1] - mean_pos[1]) ** 2)

            if hauler_comp.state == Hauler.State.IDLE:
                if dist > self.distance_tolerance:
                    hauler_comp.state = Hauler.State.MOVING_TO_PATH
                else:
                    flag_and_resource = self.get_flag_with_resource_to_pick(path_comp)
                    if not flag_and_resource:
                        continue

                    flag, resource = flag_and_resource
                    resource_comp = self.world.component_for_entity(resource, Resource)
                    if (
                            (flag == path_comp.flag1_ent and resource_comp.next_flag == path_comp.flag2_ent) or
                            (flag == path_comp.flag2_ent and resource_comp.next_flag == path_comp.flag1_ent)
                    ):
                        hauler_comp.state = Hauler.State.MOVING_TO_PICK
                    hauler_comp.flag_destination = flag
                    hauler_comp.resource_to_pick = resource

            if hauler_comp.state == Hauler.State.MOVING_TO_PATH:
                if dist < self.distance_tolerance:
                    hauler_comp.state = Hauler.State.IDLE
                else:
                    self.world.publish(MoveAgent(hauler_ent, mean_pos))

            if hauler_comp.state == Hauler.State.MOVING_TO_PICK:
                flag_pos = self.compute_flag_mean_position(hauler_comp.flag_destination)
                dist = math.sqrt((hauler_agent.pos[0] - flag_pos[0]) ** 2 + (hauler_agent.pos[1] - flag_pos[1]) ** 2)
                if dist < self.distance_tolerance:
                    hauler_comp.state = Hauler.State.PICKING_RESOURCE
                else:
                    self.world.publish(MoveAgent(hauler_ent, flag_pos))

            if hauler_comp.state == Hauler.State.PICKING_RESOURCE:
                self.world.remove_component(hauler_comp.resource_to_pick, Sprite)
                self.world.remove_component(hauler_comp.resource_to_pick, GridPosition)
                if hauler_comp.flag_destination == path_comp.flag2_ent:
                    hauler_comp.flag_destination = path_comp.flag1_ent
                else:
                    hauler_comp.flag_destination = path_comp.flag2_ent
                hauler_comp.state = Hauler.State.MOVING_TO_DROP

            if hauler_comp.state == Hauler.State.MOVING_TO_DROP:
                flag_pos = self.compute_flag_mean_position(hauler_comp.flag_destination)
                dist = math.sqrt((hauler_agent.pos[0] - flag_pos[0]) ** 2 + (hauler_agent.pos[1] - flag_pos[1]) ** 2)
                if dist < self.distance_tolerance:
                    hauler_comp.state = Hauler.State.DROPPING_RESOURCE
                else:
                    self.world.publish(MoveAgent(hauler_ent, flag_pos))

            if hauler_comp.state == Hauler.State.DROPPING_RESOURCE:
                gpx, gpy = int(hauler_agent.pos[0]), int(hauler_agent.pos[1])
                self.world.add_component(hauler_comp.resource_to_pick,
                                         Sprite(config.WOOD_SURFACE, (gpx * 16, gpy * 16)))
                self.world.add_component(hauler_comp.resource_to_pick, GridPosition(gpx, gpy))

                resource_comp = self.world.component_for_entity(hauler_comp.resource_to_pick, Resource)
                resource_comp.next_flag = None
                resource_comp.current_flag = hauler_comp.flag_destination

                hauler_comp.flag_destination = None
                hauler_comp.resource_to_pick = None
                hauler_comp.state = Hauler.State.IDLE


    def get_flag_with_resource_to_pick(self, path_comp: Path) -> Optional[Tuple[int, int]]:
        flag1, flag2 = path_comp.flag1_ent, path_comp.flag2_ent
        resources = self.world.get_component(Resource)
        for resource_ent, resource_comp in resources:
            if resource_comp.current_flag == flag1:
                return flag1, resource_ent
            if resource_comp.current_flag == flag2:
                return flag2, resource_ent
        return None

    def compute_path_mean_position(self, path_comp: Path) -> Tuple[float, float]:
        road_ents = path_comp.road_ents
        grid_pos_comps = [self.world.component_for_entity(road_ent, GridPosition) for road_ent in road_ents]
        gpxs, gpys = [gpc.pos[0] + 0.5 for gpc in grid_pos_comps], [gpc.pos[1] + 0.5 for gpc in grid_pos_comps]
        return sum(gpxs) / len(gpxs), sum(gpys) / len(gpys)

    def compute_flag_mean_position(self, flag: int) -> Tuple[float, float]:
        grid_pos_comp = self.world.component_for_entity(flag, GridPosition)
        return grid_pos_comp.pos[0] + 0.5, grid_pos_comp.pos[1] + 0.5
