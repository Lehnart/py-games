class Move:

    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy


UP = Move(0, -1)
DOWN = Move(0, 1)
LEFT = Move(-1, 0)
RIGHT = Move(1, 0)
