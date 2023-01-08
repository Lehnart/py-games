from typing import Tuple

from engine.mesper import Event


class PutFlag(Event):

    def __init__(self, grid_position: Tuple[int, int]):
        self.grid_position = grid_position
