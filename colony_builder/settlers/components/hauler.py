import enum

from mesper.mesper import Component


class Hauler(Component):
    class State(enum.Enum):
        IDLE = 1
        MOVING_TO_PATH = 2
        MOVING_TO_PICK = 3
        MOVING_TO_DROP = 4
        PICKING_RESOURCE = 5
        DROPPING_RESOURCE = 6

    def __init__(self, path_ent: int):
        self.path_ent = path_ent
        self.state = Hauler.State.IDLE
        self.flag_destination = None
        self.resource_to_pick = None
