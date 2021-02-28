from snake.logic.block import BlockType, Block
from snake.tools.direction import Direction


class Snake:
    """ Represents a Snake moving and growing"""

    def __init__(self, board, config, initial_pos_index):
        """

        :param board:
        :param config:
        :param initial_pos_index: There is 4 possible place to start the game and this index tells which one to start.
        """
        self.direction = Direction.UP
        self.board = board
        self.positions = []

        self.initial_length = int(config["LOGIC"]["initial_snake_length"])

        initial_pos = self._get_initial_pos(board, initial_pos_index)
        initial_x = initial_pos[0]
        initial_y = initial_pos[1]
        board.put_block(initial_x, initial_y, Block(BlockType.SNAKE))

        self.positions = [(initial_x, initial_y)]
        self.is_alive = True

    def get_next_head_position(self):
        """ Return the head position after next move in pysnake direction"""

        x, y = self.positions[0]
        dir = self.direction

        if dir == Direction.UP:
            y -= 1
        elif dir == Direction.DOWN:
            y += 1
        elif dir == Direction.LEFT:
            x -= 1
        elif dir == Direction.RIGHT:
            x += 1

        return x, y

    def set_direction(self, direction):
        """ Set the moving direction"""
        self.direction = direction

    def move(self):
        """ Move pysnake in the current direction """
        if len(self.positions) < self.initial_length:
            self.grow()
            return

        tail_position = self.positions.pop(-1)
        self.board.remove_block(*tail_position)

        self._move_head()

    def grow(self):
        """ Grow pysnake from one part"""
        self._move_head()

    def _move_head(self):
        head_position = self.get_next_head_position()
        self.positions = [head_position] + self.positions
        self.board.put_block(*self.positions[1], Block(BlockType.SNAKE))
        self.board.put_block(*head_position, Block(BlockType.SNAKE_HEAD))

    def _get_initial_pos(self, board, initial_pos_index):

        w = board.get_width()
        h = board.get_height()
        positions = [
            ((w // 4) - 1, (h // 4) - 1),
            ((3 * w // 4) - 1, (3 * h // 4) - 1),
            ((3 * w // 4) - 1, (h // 4) - 1),
            ((w // 4) - 1, (3 * h // 4) - 1)
        ]
        return positions[initial_pos_index]
