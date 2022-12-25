from typing import Tuple

from colony_builder.engine.mesper import Event


class MoveOnGrid(Event):

    def __init__(self, ent: int, movement: Tuple[int, int]):
        self.ent = ent
        self.movement = movement
