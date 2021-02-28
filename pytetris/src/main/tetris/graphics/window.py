import pygame

from tetris.graphics.board import Board
from tetris.graphics.score import Score


class Window:
    WIDTH = 300
    HEIGHT = 700

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((Window.WIDTH, Window.HEIGHT))
        self.board = Board(self.window)
        self.score = Score(self.window)

    def draw(self, board, score):
        self._clear()
        self.board.draw(board)
        self.score.draw(score)
        pygame.display.flip()
        
    def _clear(self):
        pygame.draw.rect(self.window, pygame.Color("black"), pygame.Rect(0, 0, Window.WIDTH, Window.HEIGHT))
