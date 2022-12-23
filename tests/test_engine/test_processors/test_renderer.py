from colony_builder.engine.components.window import Window
from colony_builder.engine.mesper import World
from colony_builder.engine.processors.renderer import Renderer


class TestRenderer:

    def test_constructor(self):
        renderer = Renderer(30)
        assert renderer.frame_per_seconds == 30

    def test_process(self):
        world = World()
        renderer = Renderer(30)
        construction_date = renderer.last_time_drawn

        world.add_processor(renderer)
        world.process()
        assert construction_date == renderer.last_time_drawn

        world.create_entity(Window((640, 480)))
        world.process()
        assert construction_date != renderer.last_time_drawn
