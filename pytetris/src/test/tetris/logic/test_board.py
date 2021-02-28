from tetris.logic.board import Board
from unittest import TestCase

class TestBoard(TestCase):

    def setUp(self):
        self.width = 10
        self.height = 20
        self.block_x = 1
        self.block_y = 2

        self.board = Board()

    def test_init(self):

        self.assertEqual(self.width, self.board.width)
        self.assertEqual(self.height, self.board.height)

        self.assertEqual(self.height, len(self.board.board))
        for row in self.board.board:
            self.assertEqual(self.width, len(row))
            [self.assertEqual(None, el) for el in row]

    def test_put_block(self):
        self.board.put_block(self.block_x, self.block_y)

        for x in range(self.width):
            for y in range(self.height):
                if x == self.block_x and y == self.block_y:
                    self.assertNotEqual(None, self.board.board[y][x])
                else:
                    self.assertEqual(None, self.board.board[y][x])

    def test_remove_block(self):
        self.board.put_block(self.block_x, self.block_y)
        self.board.remove_block(self.block_x, self.block_y)

        for x in range(self.width):
            for y in range(self.height):
                self.assertEqual(None, self.board.board[y][x])

    def test_is_block(self):
        self.board.put_block(self.block_x, self.block_y)
        for x in range(self.width):
            for y in range(self.height):
                self.assertEqual(self.board.is_block(x, y), self.board.board[y][x] is not None)

    def test_is_put_valid(self):
        self.board.put_block(self.block_x, self.block_y)
        self.assertEqual(False, self.board.is_put_valid(-1,0))
        self.assertEqual(False, self.board.is_put_valid(-1, -1))
        self.assertEqual(False, self.board.is_put_valid(0, -1))
        self.assertEqual(False, self.board.is_put_valid(9999, 0))
        self.assertEqual(False, self.board.is_put_valid(0, 9999))
        self.assertEqual(False, self.board.is_put_valid(9999, 9999))
        self.assertEqual(False, self.board.is_put_valid(self.block_x, self.block_y))
        self.assertEqual(True, self.board.is_put_valid(0, 0))

    def test_remove_full_lines(self):
        for x in range(self.width):
            for y in range(self.height):
                self.board.put_block(x, y)

        count = self.board.remove_full_lines()

        self.assertEqual(self.height, count)
        for x in range(self.width):
            for y in range(self.height):
                self.assertEqual(self.board.is_block(x, y), False)

        count = self.board.remove_full_lines()
        self.assertEqual(count,0)