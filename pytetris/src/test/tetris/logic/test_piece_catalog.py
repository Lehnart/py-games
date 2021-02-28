import unittest

from tetris.logic.piece_catalog import PieceCatalog


class TestPieceCatalog(unittest.TestCase):

    def test_get_random_piece(self):
        piece_catalog = PieceCatalog()
        generated_pieces = set([piece_catalog.get_random_piece().shape for _ in range(0, 1000)])
        self.assertEqual(len(generated_pieces), len(piece_catalog.piece_shapes))
