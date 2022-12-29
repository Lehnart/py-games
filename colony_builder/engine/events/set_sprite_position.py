from typing import Tuple

from colony_builder.engine.mesper import Event


class SetSpritePosition(Event):

    def __init__(self, ent: int, pos: Tuple[int, int]):
        self.ent = ent
        self.pos = pos
