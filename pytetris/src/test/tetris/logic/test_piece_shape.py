import unittest

from tetris.logic.piece_catalog import PieceCatalog


class TestPieceShape(unittest.TestCase):

    def test_init(self):
        t_expected = [
            [
                [True, True, True, False],
                [False, True, False, False],
                [False, False, False, False],
                [False, False, False, False]
            ],
            [
                [False, True, False, False],
                [True, True, False, False],
                [False, True, False, False],
                [False, False, False, False]
            ],
            [
                [False, True, False, False],
                [True, True, True, False],
                [False, False, False, False],
                [False, False, False, False]
            ],
            [
                [True, False, False, False],
                [True, True, False, False],
                [True, False, False, False],
                [False, False, False, False]
            ],
        ]
        self.assertEqual( PieceCatalog.t.piece_shapes , t_expected)
