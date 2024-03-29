import enum
from typing import Tuple

from mesper.mesper import Component


class Job(enum.Enum):
    HAULER = 1


class Agent(Component):

    def __init__(self, pos: Tuple[float, float], speed: float):
        self.job = None
        self.pos = pos
        self.speed = speed

    def assign_job(self, job: Job):
        self.job = job

    def move(self, move: Tuple[float, float]):
        self.pos = (self.pos[0] + move[0], self.pos[1] + move[1])
