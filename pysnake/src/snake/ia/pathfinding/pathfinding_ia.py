from snake.ia.pathfinding.graph import Graph
from snake.ia.ia import IA
from snake.tools.direction import Direction

MOVE = {(-1, 0): Direction.LEFT, (1, 0): Direction.RIGHT, (0, -1): Direction.UP, (0, 1): Direction.DOWN}

class PathFindingIA(IA):

    def __init__(self, snake_game, controller):
        super().__init__(snake_game, controller)
        self.board = snake_game.board
        self.path = None

    def next_move(self):
        if not self.path:
            graph = Graph(self.board)
            self.path = graph.get_path_by_breadth()
            if not self.path:
                return

        head_x, head_y = self._find_head_position()
        next_x, next_y, _ = self.path.pop(0)

        move = (next_x - head_x, next_y - head_y)
        self.controller.move(MOVE[move])
