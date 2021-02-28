from random import choice

from tetris.logic.piece import Piece
from tetris.logic.piece_shape import PieceShape


class PieceCatalog:
    right_l_shape = [
        ["xxoo", "xxxo", "oxoo", "xooo"],
        ["xooo", "ooxo", "oxoo", "xxxo"],
        ["xooo", "oooo", "xxoo", "oooo"],
        ["oooo", "oooo", "oooo", "oooo"]
    ]

    left_l_shape = [
        ["xxoo", "ooxo", "xooo", "xxxo"],
        ["oxoo", "xxxo", "xooo", "xooo"],
        ["oxoo", "oooo", "xxoo", "oooo"],
        ["oooo", "oooo", "oooo", "oooo"]
    ]

    right_z_shape = [
        ["xxoo", "oxoo", "xxoo", "oxoo"],
        ["oxxo", "xxoo", "oxxo", "xxoo"],
        ["oooo", "xooo", "oooo", "xooo"],
        ["oooo", "oooo", "oooo", "oooo"]
    ]

    left_z_shape = [
        ["oxxo", "xooo", "oxxo", "xooo"],
        ["xxoo", "xxoo", "xxoo", "xxoo"],
        ["oooo", "oxoo", "oooo", "oxoo"],
        ["oooo", "oooo", "oooo", "oooo"]
    ]

    i_shape = [
        ["xooo", "xxxx", "xooo", "xxxx"],
        ["xooo", "oooo", "xooo", "oooo"],
        ["xooo", "oooo", "xooo", "oooo"],
        ["xooo", "oooo", "xooo", "oooo"]
    ]

    t_shape = [
        ["xxxo", "oxoo", "oxoo", "xooo"],
        ["oxoo", "xxoo", "xxxo", "xxoo"],
        ["oooo", "oxoo", "oooo", "xooo"],
        ["oooo", "oooo", "oooo", "oooo"]
    ]

    square_shape = [
        ["xxoo", "xxoo", "xxoo", "xxoo"],
        ["xxoo", "xxoo", "xxoo", "xxoo"],
        ["oooo", "oooo", "oooo", "oooo"],
        ["oooo", "oooo", "oooo", "oooo"]
    ]

    right_l = PieceShape(right_l_shape)
    left_l = PieceShape(left_l_shape)
    right_z = PieceShape(right_z_shape)
    left_z = PieceShape(left_z_shape)
    i = PieceShape(i_shape)
    t = PieceShape(t_shape)
    square = PieceShape(square_shape)

    piece_shapes = [right_l, left_l, right_z, left_z, i, t, square]

    def __init__(self):
        pass

    def get_random_piece(self):
        random_shape = choice(PieceCatalog.piece_shapes)
        return Piece(random_shape)
