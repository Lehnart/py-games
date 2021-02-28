import random
from abc import abstractmethod

from snake.ia.ia import IA
from snake.logic.block import BlockType


class SimpleIA(IA):

    def next_move(self):
        direction = self._choose_dir()
        self.controller.move(direction)

    def _choose_dir(self):
        head_x, head_y = self._find_head_position()
        apple_x, apple_y = self._find_position(BlockType.APPLE)

        # get block types around head
        block_positions = [(head_x, head_y - 1), (head_x + 1, head_y), (head_x, head_y + 1), (head_x - 1, head_y)]
        board = self.snake_game.get_board()
        blocks = [board.get_block(*pos) for pos in block_positions]
        block_types = [b.get_type() if b is not None else None for b in blocks]

        # If apple around, let s go to the apple
        if BlockType.APPLE in block_types:
            return IA.DIRECTIONS[block_types.index(BlockType.APPLE)]

        # Else, let s avoid death
        directions = [IA.DIRECTIONS[i] for i in range(len(block_types)) if block_types[i] not in IA.DEATH_BLOCK_TYPES]
        if len(directions) == 0:
            return random.choice(IA.DIRECTIONS)

        # If there is still choice, try to get closer to the apple
        to_apple_distances = self.distance_to_apple(block_positions, (apple_x, apple_y))
        min_distance = None
        best_direction = None
        for direction in directions:
            index = IA.DIRECTIONS.index(direction)
            distance = to_apple_distances[index]
            if min_distance is None or distance < min_distance:
                min_distance = distance
                best_direction = direction

        return best_direction

    @abstractmethod
    def distance_to_apple(self, block_positions, apple_position):
        pass

    def _find_position(self, block_type):
        board = self.snake_game.get_board().board
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] is None:
                    continue

                if board[y][x].type == block_type:
                    return x, y
