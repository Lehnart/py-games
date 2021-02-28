import pygame

from snake.logic.block import BlockType


class Board:

    def __init__(self, window, config):
        """
        :param window:
        """
        self.window = window

        self.width = self.window.get_width()
        self.height = self.window.get_height()

        self._read_config(config)

    def draw(self, board):
        """
        Draw a board in the window given as parameter of the constructor
        :param board: board to be drawn
        :return:
        """
        w = board.get_width()
        h = board.get_height()

        block_width = int(self.width / w)
        block_height = int(self.height / h)

        for y in range(h):
            for x in range(w):
                b = board.get_block(x, y)
                if board.get_block(x, y) is not None:
                    self._draw_block((x, y), (block_width, block_height, b.get_type()))

    def _draw_block(self, pos, block):
        x0 = 0
        y0 = 0

        x, y = pos
        block_w, block_h, block_type = block

        x_pix = (x * block_w) + x0 + 2
        y_pix = (y * block_h) + y0 + 2
        pygame.draw.rect(
            self.window,
            self.block_color_by_type[block_type],
            pygame.Rect(x_pix, y_pix, block_w - 4, block_h - 4)
        )

    def _read_config(self,config):

        apple_color = pygame.Color(config["GRAPHICS"]["apple_color"])
        snake_color = pygame.Color(config["GRAPHICS"]["snake_color"])
        snake_head_color = pygame.Color(config["GRAPHICS"]["snake_head_color"])
        wall_color = pygame.Color(config["GRAPHICS"]["wall_color"])

        self.block_color_by_type = {
            BlockType.APPLE: apple_color,
            BlockType.SNAKE: snake_color,
            BlockType.SNAKE_HEAD: snake_head_color,
            BlockType.WALL: wall_color}

