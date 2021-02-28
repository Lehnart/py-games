import pygame


class Board:
    BLOCK_COLOR = pygame.Color("blue")
    BOARD_RECT = pygame.Rect(0, 100, 300, 600)

    def __init__(self, window):
        """
        :param window:
        """
        self.window = window

    def draw(self, board):
        """
        Draw a board in the window given as parameter of the constructor
        :param board: board to be drawn
        :return:
        """
        w = board.get_width()
        h = board.get_height()

        block_width = int(Board.BOARD_RECT.width / w)
        block_height = int(Board.BOARD_RECT.height / h)

        for y in range(h):
            for x in range(w):
                if board.is_block(x, y):
                    self._draw_block(x, y, block_width, block_height)

    def _draw_block(self, x, y, block_width, block_height):
        x0 = Board.BOARD_RECT.x
        y0 = Board.BOARD_RECT.y

        x_pix = (x * block_width) + x0
        y_pix = (y * block_height) + y0
        pygame.draw.rect(self.window, pygame.Color("blue"), pygame.Rect(x_pix, y_pix, block_width, block_height))
