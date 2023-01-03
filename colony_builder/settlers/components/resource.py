import enum

from colony_builder.engine.mesper import Component


class ResourceType(enum.Enum):
    WOOD = 1


class Resource(Component):

    def __init__(self, resource_type: ResourceType):
        self.resource_type = resource_type
        self.destination = None
        self.next_flag = None
