from mesper. components.grid_position import GridPosition
from mesper.mesper import World
from colony_builder.settlers.components.flag import Flag
from colony_builder.settlers.components.path import Path
from colony_builder.settlers.components.resource import Resource, ResourceType
from colony_builder.settlers.components.resource_destination import ResourceDestination
from colony_builder.settlers.components.road import Road
from colony_builder.settlers.processors.resource_path_planner import ResourcePathPlanner


class TestResourcePathPlaner:

    def prepare_world(self):
        self.world = World()
        self.processor = ResourcePathPlanner()
        self.world.add_processor(self.processor)
        roads_path1 = [self.world.create_entity(Road(), GridPosition(x, 0)) for x in range(4)]
        roads_path2 = [self.world.create_entity(Road(), GridPosition(3, y)) for y in range(4)]
        self.flag1 = self.world.create_entity(Flag(), ResourceDestination(), GridPosition(0, 0))
        self.flag2 = self.world.create_entity(Flag(), GridPosition(3, 0))
        self.flag3 = self.world.create_entity(Flag(), GridPosition(3, 3))
        self.path1 = self.world.create_entity(Path(self.flag1, self.flag2, roads_path1))
        self.path2 = self.world.create_entity(Path(self.flag3, self.flag2, roads_path2))
        self.resource = self.world.create_entity(Resource(ResourceType.WOOD), GridPosition(3, 3))
        self.resource_out_of_flag = self.world.create_entity(Resource(ResourceType.WOOD), GridPosition(4, 5))

    def test_get_positions_with_flags(self):
        self.prepare_world()
        pos_with_flags = self.processor.get_positions_with_flag()
        assert pos_with_flags[(0, 0)] == self.flag1
        assert pos_with_flags[(3, 0)] == self.flag2
        assert pos_with_flags[(3, 3)] == self.flag3

    def test_construct_path_graph(self):
        self.prepare_world()
        path_graph = self.processor.construct_path_graph()
        assert path_graph[self.flag1] == {self.flag2: 3}
        assert path_graph[self.flag2] == {self.flag1: 3, self.flag3: 3}
        assert path_graph[self.flag3] == {self.flag2: 3}

    def test_find_path(self):
        self.prepare_world()
        path_graph = self.processor.construct_path_graph()
        paths = self.processor.find_path(self.flag3, self.flag1, path_graph)
        assert paths == [[self.flag3, self.flag2, self.flag1]]

    def test_process(self):
        self.prepare_world()
        self.world.process()
        resource_comp = self.world.component_for_entity(self.resource, Resource)
        assert resource_comp.resource_type == ResourceType.WOOD
        assert resource_comp.destination == self.flag1
        assert resource_comp.next_flag == self.flag2

        resource_out_comp = self.world.component_for_entity(self.resource_out_of_flag, Resource)
        assert resource_out_comp.resource_type == ResourceType.WOOD
        assert resource_out_comp.destination is None
        assert resource_out_comp.next_flag is None
