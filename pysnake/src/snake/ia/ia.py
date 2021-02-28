from abc import ABC, abstractmethod

from snake.logic.block import BlockType
from snake.tools.direction import Direction


class IA(ABC):
    DIRECTIONS = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
    DEATH_BLOCK_TYPES = [BlockType.SNAKE_HEAD, BlockType.SNAKE, BlockType.WALL]

    def __init__(self, snake_game, controller):
        self.snake_game = snake_game
        self.controller = controller
        self.snake = controller.snake

    @abstractmethod
    def next_move(self):
        pass

    def _find_head_position(self):
        return self.snake.positions[0]
