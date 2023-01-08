import math
from typing import Tuple, List

from engine.components.grid_position import GridPosition
from engine.components.sprite import Sprite
from engine.mesper import Processor
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
        for hauler_ent, [hauler_comp, agent_comp] in haulers:
            path_comp = self.world.component_for_entity(hauler_comp.path_ent, Path)

            if hauler_comp.state == Hauler.State.IDLE:
                self.process_idle_state(hauler_comp, agent_comp, path_comp)

            elif hauler_comp.state == Hauler.State.MOVING_TO_PATH:
                self.process_moving_to_path(hauler_ent, hauler_comp, agent_comp, path_comp)

            elif hauler_comp.state == Hauler.State.MOVING_TO_PICK:
                self.process_moving_to_pick_state(hauler_ent, hauler_comp, agent_comp)

            elif hauler_comp.state == Hauler.State.PICKING_RESOURCE:
                self.process_picking_resource_state(hauler_comp, path_comp)

            elif hauler_comp.state == Hauler.State.MOVING_TO_DROP:
                self.process_moving_to_drop(hauler_ent, hauler_comp, agent_comp)

            elif hauler_comp.state == Hauler.State.DROPPING_RESOURCE:
                self.process_dropping_resource(hauler_comp, agent_comp)

    def process_idle_state(self, hauler_comp: Hauler, agent_comp: Agent, path_comp: Path):

        mean_pos = self.compute_path_mean_position(path_comp)
        dist = math.sqrt((agent_comp.pos[0] - mean_pos[0]) ** 2 + (agent_comp.pos[1] - mean_pos[1]) ** 2)
        if dist > self.distance_tolerance:
            hauler_comp.state = Hauler.State.MOVING_TO_PATH
        else:
            flags_and_resources = self.get_flag_with_resource_to_pick(path_comp)
            if not flags_and_resources:
                return

            for flag, resource in flags_and_resources:
                resource_comp = self.world.component_for_entity(resource, Resource)
                if (
                        (flag == path_comp.flag1_ent and resource_comp.next_flag == path_comp.flag2_ent) or
                        (flag == path_comp.flag2_ent and resource_comp.next_flag == path_comp.flag1_ent)
                ):
                    hauler_comp.state = Hauler.State.MOVING_TO_PICK
                    hauler_comp.flag_destination = flag
                    hauler_comp.resource_to_pick = resource
                    break

    def process_moving_to_path(self, ent: int, hauler_comp: Hauler, agent_comp: Agent, path_comp: Path):
        mean_pos = self.compute_path_mean_position(path_comp)
        dist = math.sqrt((agent_comp.pos[0] - mean_pos[0]) ** 2 + (agent_comp.pos[1] - mean_pos[1]) ** 2)

        if dist < self.distance_tolerance:
            hauler_comp.state = Hauler.State.IDLE
        else:
            self.world.publish(MoveAgent(ent, mean_pos))

    def process_moving_to_pick_state(self, ent: int, hauler_comp: Hauler, agent_comp: Agent):
        is_close, flag_pos = self.check_distance_to_destination_flag(hauler_comp, agent_comp)
        if is_close:
            hauler_comp.state = Hauler.State.PICKING_RESOURCE
        else:
            self.world.publish(MoveAgent(ent, flag_pos))

    def process_picking_resource_state(self, hauler_comp: Hauler, path_comp: Path):
        self.world.remove_component(hauler_comp.resource_to_pick, Sprite)
        self.world.remove_component(hauler_comp.resource_to_pick, GridPosition)
        if hauler_comp.flag_destination == path_comp.flag2_ent:
            hauler_comp.flag_destination = path_comp.flag1_ent
        else:
            hauler_comp.flag_destination = path_comp.flag2_ent
        hauler_comp.state = Hauler.State.MOVING_TO_DROP

    def process_moving_to_drop(self, ent: int, hauler_comp: Hauler, agent_comp: Agent):
        is_close, flag_pos = self.check_distance_to_destination_flag(hauler_comp, agent_comp)
        if is_close:
            hauler_comp.state = Hauler.State.DROPPING_RESOURCE
        else:
            self.world.publish(MoveAgent(ent, flag_pos))

    def process_dropping_resource(self, hauler_comp: Hauler, agent_comp: Agent):
        gpx, gpy = int(agent_comp.pos[0]), int(agent_comp.pos[1])
        self.world.add_component(hauler_comp.resource_to_pick,
                                 Sprite(config.WOOD_SURFACE, (gpx * 16, gpy * 16)))
        self.world.add_component(hauler_comp.resource_to_pick, GridPosition(gpx, gpy))

        resource_comp = self.world.component_for_entity(hauler_comp.resource_to_pick, Resource)
        resource_comp.next_flag = None
        resource_comp.current_flag = hauler_comp.flag_destination

        hauler_comp.flag_destination = None
        hauler_comp.resource_to_pick = None
        hauler_comp.state = Hauler.State.IDLE

    def get_flag_with_resource_to_pick(self, path_comp: Path) -> List[Tuple[int, int]]:
        flags_and_resources = []
        flag1, flag2 = path_comp.flag1_ent, path_comp.flag2_ent
        resources = self.world.get_component(Resource)
        for resource_ent, resource_comp in resources:
            if resource_comp.current_flag == flag1:
                flags_and_resources.append((flag1, resource_ent))
            if resource_comp.current_flag == flag2:
                flags_and_resources.append((flag2, resource_ent))
        return flags_and_resources

    def check_distance_to_destination_flag(self, hauler_comp: Hauler, agent_comp: Agent):
        flag_pos = self.compute_flag_mean_position(hauler_comp.flag_destination)
        dist = math.sqrt((agent_comp.pos[0] - flag_pos[0]) ** 2 + (agent_comp.pos[1] - flag_pos[1]) ** 2)
        return dist < self.distance_tolerance

    def compute_flag_mean_position(self, flag: int) -> Tuple[float, float]:
        grid_pos_comp = self.world.component_for_entity(flag, GridPosition)
        return grid_pos_comp.pos[0] + 0.5, grid_pos_comp.pos[1] + 0.5

    def compute_path_mean_position(self, path_comp: Path) -> Tuple[float, float]:
        road_ents = path_comp.road_ents
        grid_pos_comps = [self.world.component_for_entity(road_ent, GridPosition) for road_ent in road_ents]
        gpxs, gpys = [gpc.pos[0] + 0.5 for gpc in grid_pos_comps], [gpc.pos[1] + 0.5 for gpc in grid_pos_comps]
        return sum(gpxs) / len(gpxs), sum(gpys) / len(gpys)
