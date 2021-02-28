import pygame

from snake.graphics.board import Board


class Window:
    def __init__(self, config):
        pygame.init()

        self.width = int(config["GRAPHICS"]["board_rect_width"])
        self.height = int(config["GRAPHICS"]["board_rect_height"])

        self.window = pygame.display.set_mode((self.width, self.height))
        self.board = Board(self.window, config)

    def draw(self, board):
        self._clear()
        self.board.draw(board)
        pygame.display.flip()
        
    def _clear(self):
        pygame.draw.rect(self.window, pygame.Color("black"), pygame.Rect(0, 0, self.width, self.height))
