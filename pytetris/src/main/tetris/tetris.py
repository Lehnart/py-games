from tetris.controller.controller import Controller
from tetris.graphics.window import Window
from tetris.logic.board import Board
from tetris.logic.rules import Rules


class Tetris:

    def __init__(self):
        self.is_game_over = False
        self.board = Board()
        self.window = Window()
        self.rules = Rules(self)
        self.controller = Controller(self)

    def move(self, direction):
        self.rules.move(direction)
        self.window.draw(self.board, self.rules.get_score())

    def rotate(self, rotation):
        self.rules.rotate(rotation)
        self.window.draw(self.board, self.rules.get_score())

    def game_over(self):
        self.is_game_over = True

    def is_over(self):
        return self.is_game_over
