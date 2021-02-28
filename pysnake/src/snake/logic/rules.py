import random

from snake.logic.block import BlockType, Block
from snake.logic.snake import Snake
from snake.tools.timer import Timer


class Rules:

    def __init__(self, board, snake_game, config):
        self.board = board
        self.snakeGame = snake_game

        self.snakes = []
        for i in range(int(config["LOGIC"]["snake_count"])):
            self.snakes.append(Snake(board, config, i))

        self.max_moves_without_apple = int(config["LOGIC"]["max_moves_without_apple"])
        self.moves_count_wo_apple_per_snake = [0 for _ in range(len(self.snakes))]
        self.apple_eat_per_snake = [0 for _ in range(len(self.snakes))]
        self.move_per_snake = [0 for _ in range(len(self.snakes))]

        self._put_apple()

    def update(self):
        for snake_index in range(len(self.snakes)):
            self._update_snake(snake_index)

        if all([not snake.is_alive for snake in self.snakes]):
            self.snakeGame.game_over()

    def _update_snake(self, snake_index):
        snake = self.snakes[snake_index]

        if not snake.is_alive:
            return

        next_head_position = snake.get_next_head_position()
        block = self.board.get_block(*next_head_position)

        if block is None:
            snake.move()
            self.move_per_snake[snake_index] += 1

            self.moves_count_wo_apple_per_snake[snake_index] += 1
            if self.moves_count_wo_apple_per_snake[snake_index] > self.max_moves_without_apple :
                self._kill_snake(snake)

        elif block.get_type() is BlockType.APPLE:
            snake.grow()
            self.apple_eat_per_snake[snake_index] += 1
            self.moves_count_wo_apple_per_snake[snake_index] = 0
            self._put_apple()

        elif block.get_type() in [BlockType.SNAKE, BlockType.WALL]:
            self._kill_snake(snake)

    def move(self, direction, snake):
        snake.set_direction(direction)

    def _put_apple(self):
        positions = self.board.get_empty_block_positions()
        random_pos = random.choice(positions)
        self.board.put_block(*random_pos, Block(BlockType.APPLE))

    def _kill_snake(self, snake):

        # Snake blocks are replaced by walls
        for pos in snake.positions:
            self.board.put_block(*pos, Block(BlockType.WALL))
        snake.is_alive = False
