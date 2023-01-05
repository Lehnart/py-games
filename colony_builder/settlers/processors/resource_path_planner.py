from typing import Dict, List

from colony_builder.engine.components.grid_position import GridPosition
from colony_builder.engine.mesper import Processor
from colony_builder.settlers.components.flag import Flag
from colony_builder.settlers.components.path import Path
from colony_builder.settlers.components.resource import Resource
from colony_builder.settlers.components.resource_destination import ResourceDestination


class ResourcePathPlanner(Processor):

    def process(self):

        resource_destinations = self.world.get_components(Flag, ResourceDestination, GridPosition)
        flag_dest_ent, [_, _, _] = resource_destinations[0]

        path_graph = None
        positions_with_flag = self.get_positions_with_flag()

        resources = self.world.get_components(Resource, GridPosition)
        for _, [resource_comp, resource_pos] in resources:

            if resource_pos.pos not in positions_with_flag:
                continue
            flag_src_ent = positions_with_flag[resource_pos.pos]

            if resource_comp.destination is None:
                resource_comp.destination = flag_dest_ent

            if resource_comp.next_flag is None:
                if not path_graph:
                    path_graph = self.construct_path_graph()

                resource_paths = self.find_path(flag_src_ent, flag_dest_ent, path_graph)
                resource_comp.next_flag = resource_paths[0][1]

    def construct_path_graph(self) -> Dict[int, Dict[int, int]]:
        graph = {}
        paths = self.world.get_component(Path)
        for _, path_comp in paths:
            flag1_ent, flag2_ent = path_comp.flag1_ent, path_comp.flag2_ent

            if flag1_ent not in graph:
                graph[flag1_ent] = {}
            graph[flag1_ent][flag2_ent] = path_comp.length()

            if flag2_ent not in graph:
                graph[flag2_ent] = {}
            graph[flag2_ent][flag1_ent] = path_comp.length()
        return graph

    def get_positions_with_flag(self):
        pos_with_flags = {}
        flags = self.world.get_components(GridPosition, Flag)
        for flag_ent, [flag_pos, _] in flags:
            pos_with_flags[flag_pos.pos] = flag_ent

        return pos_with_flags

    def find_path(self, flag1: int, flag2: int, path_graph: Dict[int, Dict[int, int]], path: List[int] = None):

        if path is None:
            path = []

        path = path + [flag1]
        if flag1 == flag2:
            return [path]

        paths = []

        for flag in path_graph[flag1]:
            if flag not in path:
                subpaths = self.find_path(flag, flag2, path_graph, path)
                for subpath in subpaths:
                    paths.append(subpath)
        return paths
