from unittest import TestCase

from tetris.logic.board import Board
from tetris.logic.rules import Rules
from tetris.tools.direction import Direction
from tetris.tools.rotation import Rotation


class DummyTetris:
    """Class without graphics and controller parts for test"""
    WIDTH = 7
    HEIGHT = 21

    def __init__(self):
        self.is_game_over = False
        self.board = Board()
        self.rules = Rules(self)

    def move(self, direction):
        self.rules.move(direction)

    def rotate(self, rotation):
        self.rules.move(rotation)

    def game_over(self):
        exit()


class TestRules(TestCase):

    def setUp(self):
        self.tetris = DummyTetris()
        self.rules = self.tetris.rules
        self.board = self.rules._get_board()

    def test_init(self):
        count = 0
        for y in range(len(self.board.board)):
            for x in range(len(self.board.board[y])):
                case = self.board.board[y][x]
                if x < self.rules._get_initial_piece_pos()[0]:
                    self.assertEqual(case, None)
                if case is not None:
                    count += 1
        self.assertEqual(count, 4)

    def test_move(self):
        results = []
        with self.assertRaises(SystemExit):
            for i in range(200):
                results.append(self.rules.move(Direction.DOWN))

    def test_rotate(self):
        self.rules.move(Direction.DOWN)
        self.rules.move(Direction.DOWN)

        start_positions = []
        for y in range(len(self.board.board)):
            for x in range(len(self.board.board[y])):
                if self.board.board[y][x]:
                    start_positions.append((x, y))

        for i in range(10):
            self.rules.rotate(Rotation.CLOCKWISE)
            self.assertEqual(self.rules.piece.rotation_index, (i + 1) % 4)

        for i in range(9):
            self.rules.rotate(Rotation.COUNTER_CLOCKWISE)
            self.assertEqual(self.rules.piece.rotation_index, (10 - i - 1) % 4)

        count = 0
        for y in range(len(self.board.board)):
            for x in range(len(self.board.board[y])):
                if self.board.board[y][x] is not None:
                    count += 1

        self.assertEqual(count, 4)
