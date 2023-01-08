from colony_builder.engine.components.grid_position import GridPosition
from colony_builder.engine.mesper import World
from colony_builder.settlers.components.agent import Agent
from colony_builder.settlers.components.flag import Flag
from colony_builder.settlers.components.hauler import Hauler
from colony_builder.settlers.components.path import Path
from colony_builder.settlers.components.resource import Resource, ResourceType
from colony_builder.settlers.events.move_agent import MoveAgent
from colony_builder.settlers.processors.hauler_updater import HaulerUpdater
from tests.test_settlers.test_components.test_path import TestPath


class TestHaulerUpdater:

    def test_process(self):
        world = World()
        hauler_updater = HaulerUpdater()
        world.add_processor(hauler_updater)

        path = TestPath.create_test_path(world)

        hauler = world.create_entity(Hauler(path), Agent((0, 0), 1.))
        world.process()  # Changing state from idle to moving
        world.process()  # Start moving

        move_agent_events = world.receive(MoveAgent)
        assert len(move_agent_events) == 1
        move_agent_event = move_agent_events[0]
        assert move_agent_event.agent_ent == hauler
        assert move_agent_event.destination[0] == 1.5
        assert move_agent_event.destination[1] == 0.5

    def test_compute_mean_position(self):
        world = World()
        hauler_updater = HaulerUpdater()
        world.add_processor(hauler_updater)
        path = TestPath.create_test_path(world)
        path_comp = world.component_for_entity(path, Path)
        mean_pos_x, mean_pos_y = hauler_updater.compute_path_mean_position(path_comp)
        assert mean_pos_x == 1.5
        assert mean_pos_y == 0.5

    def test_compute_path_position(self):
        world = World()
        hauler_updater = HaulerUpdater()
        world.add_processor(hauler_updater)
        flag = world.create_entity(Flag(), GridPosition(1, 3))
        mean_pos_x, mean_pos_y = hauler_updater.compute_flag_mean_position(flag)
        assert mean_pos_x == 1.5
        assert mean_pos_y == 3.5

    def test_check_distance_to_destination_flag(self):
        world = World()
        hauler_updater = HaulerUpdater()
        world.add_processor(hauler_updater)
        path = TestPath.create_test_path(world)
        hauler_ent = world.create_entity(Hauler(path), Agent((0., 1.), 5.))
        flags = world.get_components(Flag, GridPosition)
        flag_dest = None
        for flag_ent, [_, grid_pos_comp] in flags:
            if grid_pos_comp.pos[0] == 2 and grid_pos_comp.pos[1] == 0:
                flag_dest = flag_ent

        hauler_comp = world.component_for_entity(hauler_ent, Hauler)
        hauler_comp.flag_destination = flag_dest
        agent_comp = world.component_for_entity(hauler_ent, Agent)
        assert not hauler_updater.check_distance_to_destination_flag(hauler_comp, agent_comp)

        agent_comp.pos = (2.5, 0.5)
        assert hauler_updater.check_distance_to_destination_flag(hauler_comp, agent_comp)

    def test_flag_with_resource_to_pick(self):
        world = World()
        hauler_updater = HaulerUpdater()
        world.add_processor(hauler_updater)
        path = TestPath.create_test_path(world)
        path_comp = world.component_for_entity(path, Path)
        resource_comp = Resource(ResourceType.WOOD)
        resource_comp.current_flag = path_comp.flag1_ent
        resource_comp.destination = path_comp.flag2_ent
        resource_comp.next_flag = path_comp.flag2_ent

        resource_ent = world.create_entity(resource_comp)
        assert hauler_updater.get_flag_with_resource_to_pick(path_comp) == [(path_comp.flag1_ent, resource_ent)]
