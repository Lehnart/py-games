import enum
from typing import Tuple

from colony_builder.engine.mesper import Component


class Job(enum.Enum):
    HAULER = 1


class Agent(Component):

    def __init__(self, pos: Tuple[float, float], speed: Tuple[float, float]):
        self.job = None
        self.pos = pos
        self.speed = speed

    def assign_job(self, job: Job):
        self.job = job

    def move(self, move: Tuple[float, float]):
        self.pos = (self.pos[0] + move[0], self.pos[1] + move[1])
