from colony_builder.engine.mesper import Processor
from colony_builder.settlers.components.path import Path
from colony_builder.settlers.events.need_hauler import NeedHauler


class PathAssigner(Processor):

    def process(self):

        paths = self.world.get_component(Path)
        for path_ent, path_comp in paths:
            if path_comp.worker_ent is None:
                self.world.publish(NeedHauler(path_ent))
