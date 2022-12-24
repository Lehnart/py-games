import pygame.event
import pytest

from colony_builder.engine.components.keyboard_input import KeyboardInput
from colony_builder.engine.mesper import World, Event
from colony_builder.engine.processors.updater import Updater


class TestUpdater:
    class MyEvent(Event):
        pass

    def init_world(self):
        pygame.init()

        world = World()
        updater = Updater()
        world.add_processor(updater)
        return world

    def test_process(self):
        world = self.init_world()
        world.process()

        pygame.event.post(pygame.event.Event(pygame.QUIT))
        with pytest.raises(SystemExit):
            world.process()

    def test_event_key_pressed(self):
        world = self.init_world()
        world.create_entity(KeyboardInput({pygame.K_z: lambda ent, w: w.publish(TestUpdater.MyEvent())}))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_z}))

        events = world.receive(TestUpdater.MyEvent)
        assert len(events) == 0

        world.process()
        events = world.receive(TestUpdater.MyEvent)
        assert len(events) == 1
        assert isinstance(events[0], TestUpdater.MyEvent)
