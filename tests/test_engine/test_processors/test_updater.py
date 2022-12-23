import pygame.event
import pytest

from colony_builder.engine.mesper import World
from colony_builder.engine.processors.updater import Updater


class TestUpdater:

    def test_process(self):
        pygame.init()

        world = World()
        updater = Updater()
        world.add_processor(updater)

        world.process()

        pygame.event.post(pygame.event.Event(pygame.QUIT))
        with pytest.raises(SystemExit):
            world.process()
