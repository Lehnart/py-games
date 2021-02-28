from tetris.logic.block import Block


class Board:
    """ Represents a physical board containing blocks in a 2D array"""

    WIDTH = 10
    HEIGHT = 20

    def __init__(self):
        self.width = Board.WIDTH
        self.height = Board.HEIGHT

        self.board = [[None for _ in range(self.width)] for _ in range(self.height)]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def put_block(self, x, y):
        """
        :param x: 0 <= x < height
        :param y: 0 <= y < width
        :return:
        """
        self.board[y][x] = Block()

    def remove_block(self, x, y):
        """
        :param x: 0 <= x < height
        :param y: 0 <= y < width
        :return:
        """
        self.board[y][x] = None

    def is_put_valid(self, x, y):
        """
        :param x: 0 <= x < height
        :param y: 0 <= y < width
        :return:
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False

        return self.board[y][x] is None

    def is_block(self, x, y):
        """
        :param x: 0 <= x < height
        :param y: 0 <= y < width
        :return:
        """
        return self.board[y][x] is not None

    def remove_full_lines(self):
        """
        Remove all lines which are full
        :return: number of full lines
        """

        # find full lines
        ys = []
        for y in range(len(self.board)):
            if all(self.is_block(x, y) for x in range(len(self.board[y]))):
                ys.append(y)

        # remove full lines
        for full_y in ys:
            [self.remove_block(x, full_y) for x in range(len(self.board[full_y]))]

            # drop lines
            for y in range(full_y, 0, -1):
                for x in range(len(self.board[y])):
                    self.board[y][x] = self.board[y - 1][x]

        return len(ys)