from typing import Tuple

from engine.mesper import Event


class MoveAgent(Event):

    def __init__(self, agent_ent: int, destination: Tuple[float, float]):
        self.agent_ent = agent_ent
        self.destination = destination
