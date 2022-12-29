from colony_builder.engine.mesper import Component


class Hauler(Component):

    def __init__(self, path_ent: int):
        self.path_ent = path_ent
