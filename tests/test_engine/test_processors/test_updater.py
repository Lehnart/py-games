import pygame.event
import pytest

from colony_builder.engine.mesper import World
from colony_builder.engine.processors.updater import Updater


class TestUpdater:

    def test_process(self):
        world = World()
        updater = Updater()
        world.add_processor(updater)

        pygame.init()
        pygame.event.post(pygame.event.Event(pygame.QUIT))

        with pytest.raises(SystemExit):
            world.process()
