from typing import Tuple

from mesper.mesper import Event


class PutFlag(Event):

    def __init__(self, grid_position: Tuple[int, int]):
        self.grid_position = grid_position
