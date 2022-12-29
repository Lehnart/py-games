from colony_builder.engine.mesper import Event


class NeedHauler(Event):

    def __init__(self, path_ent: int):
        self.path_ent = path_ent
