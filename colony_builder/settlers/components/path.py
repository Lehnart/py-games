from typing import List

from colony_builder.engine.mesper import Component


class Path(Component):

    def __init__(self, flag1_ent: int, flag2_ent: int, road_ents: List[int]):
        self.flag1_ent = flag1_ent
        self.flag2_ent = flag2_ent
        self.road_ents = road_ents
        self.worker_ent = None

    def assign_worker(self, worker_ent: int):
        self.worker_ent = worker_ent
