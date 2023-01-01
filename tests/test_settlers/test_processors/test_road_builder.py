from colony_builder.engine.components.grid_position import GridPosition
from colony_builder.engine.mesper import World
from colony_builder.settlers.components.flag import Flag
from colony_builder.settlers.components.path import Path
from colony_builder.settlers.components.road import Road
from colony_builder.settlers.events.put_flag import PutFlag
from colony_builder.settlers.processors.road_builder import RoadBuilder


class TestRoadBuilder:

    def prepare_world(self):
        world = World()
        road_builder = RoadBuilder()
        world.add_processor(road_builder)

        world.publish(PutFlag((0, 0)))
        world.process()

        return world, road_builder

    def test_put_flag_properly(self):
        world, road_builder = self.prepare_world()

        assert road_builder.is_first_flag_set is True
        assert road_builder.flag1_ent is not None
        assert world.component_for_entity(road_builder.flag1_ent, GridPosition).pos == (0, 0)
        assert len(world.get_component(Road)) == 0
        assert len(world.get_component(Path)) == 0
        assert len(world.get_component(Flag)) == 1

        world.publish(PutFlag((3, 0)))
        world.process()
        assert road_builder.is_first_flag_set is False
        assert road_builder.flag1_ent is None
        assert len(world.get_component(GridPosition)) == 6
        assert len(world.get_component(Road)) == 4
        assert len(world.get_component(Flag)) == 2
        assert len(world.get_component(Path)) == 1
        [[_, path]] = world.get_component(Path)
        assert len(path.road_ents) == 4

    def test_put_flag_not_on_straight_line(self):
        world, road_builder = self.prepare_world()

        world.publish(PutFlag((3, 3)))
        world.process()
        world.process()

        assert road_builder.is_first_flag_set is False
        assert road_builder.flag1_ent is None
        assert len(world.get_component(GridPosition)) == 0
        assert len(world.get_component(Flag)) == 0
        assert len(world.get_component(Road)) == 0
        assert len(world.get_component(Path)) == 0

    def test_unvalid_path_length(self):
        world, road_builder = self.prepare_world()

        world.publish(PutFlag((1, 0)))
        world.publish(PutFlag((0, 0)))
        world.publish(PutFlag((0, 1)))

        world.publish(PutFlag((0, 0)))
        world.publish(PutFlag((0, 7)))

        world.publish(PutFlag((7, 0)))
        world.publish(PutFlag((0, 0)))
        world.process()
        world.process()

        assert road_builder.is_first_flag_set is False
        assert road_builder.flag1_ent is None
        assert len(world.get_component(GridPosition)) == 0
        assert len(world.get_component(Flag)) == 0
        assert len(world.get_component(Road)) == 0
        assert len(world.get_component(Path)) == 0

    def test_do_not_delete_1st_flag_if_it_was_already_existing(self):
        world, road_builder = self.prepare_world()

        world.publish(PutFlag((0, 3)))
        world.publish(PutFlag((0, 0)))
        world.publish(PutFlag((3, 3)))
        world.process()
        world.process()

        assert road_builder.is_first_flag_set is False
        assert road_builder.flag1_ent is None
        assert len(world.get_component(GridPosition)) == 6
        assert len(world.get_component(Flag)) == 2
        assert len(world.get_component(Road)) == 4
        assert len(world.get_component(Path)) == 1

    def test_put_first_flag_on_existing_flag(self):
        world, road_builder = self.prepare_world()
        world.publish(PutFlag((3, 0)))
        world.publish(PutFlag((0, 0)))
        world.publish(PutFlag((0, 3)))

        world.process()
        world.process()

        assert road_builder.is_first_flag_set is False
        assert road_builder.flag1_ent is None
        assert len(world.get_component(Flag)) == 3
        assert len(world.get_component(Road)) == 7
        assert len(world.get_component(Path)) == 2

    def test_put_second_flag_on_existing_flag(self):
        world, road_builder = self.prepare_world()
        world.publish(PutFlag((3, 0)))
        world.publish(PutFlag((0, 3)))
        world.publish(PutFlag((0, 0)))

        world.process()
        world.process()

        assert road_builder.is_first_flag_set is False
        assert road_builder.flag1_ent is None
        assert len(world.get_component(Flag)) == 3
        assert len(world.get_component(Road)) == 7
        assert len(world.get_component(Path)) == 2
