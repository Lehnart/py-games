from colony_builder.engine.mesper import Component


class GridPosition(Component):

    def __init__(self, pos_x: int, pos_y: int):
        self.pos = (pos_x, pos_y)

    def move(self, move_x: int, move_y: int):
        pos_x, pos_y = self.pos
        pos_x += move_x
        pos_y += move_y
        self.pos = (pos_x, pos_y)
