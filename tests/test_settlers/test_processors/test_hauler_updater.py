from colony_builder.engine.mesper import World
from colony_builder.settlers.components.agent import Agent
from colony_builder.settlers.components.hauler import Hauler
from colony_builder.settlers.events.move_agent import MoveAgent
from colony_builder.settlers.processors.hauler_updater import HaulerUpdater
from tests.test_settlers.test_components.test_path import TestPath


class TestHaulerUpdater:

    def test_process(self):
        world = World()
        hauler_updater = HaulerUpdater()
        world.add_processor(hauler_updater)

        path = TestPath.create_test_path(world)

        hauler = world.create_entity(Hauler(path), Agent((0,0), 1.))
        world.process()

        move_agent_events = world.receive(MoveAgent)
        assert len(move_agent_events) == 1
        move_agent_event = move_agent_events[0]
        assert move_agent_event.agent_ent == hauler
        assert move_agent_event.destination[0] == 1.5
        assert move_agent_event.destination[1] == 0.5
