from mesper.mesper import World
from colony_builder.settlers.components.path import Path
from colony_builder.settlers.events.need_hauler import NeedHauler
from colony_builder.settlers.processors.path_assigner import PathAssigner
from tests.test_colony_builder.test_settlers.test_components.test_path import TestPath


class TestPathAssigner:

    def test_process(self):
        world = World()

        path_assigner = PathAssigner()
        world.add_processor(path_assigner)

        path = TestPath.create_test_path(world)

        world.process()
        need_hauler_events = world.receive(NeedHauler)
        assert len(need_hauler_events) == 1
        need_hauler_event = need_hauler_events[0]
        assert need_hauler_event.path_ent == path

        path_comp = world.component_for_entity(path, Path)
        path_comp.worker_ent = 999

        world.process()
        world.process()
        need_hauler_events = world.receive(NeedHauler)
        assert len(need_hauler_events) == 0
