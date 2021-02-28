from snake.logic.block import Block, BlockType


class Board:
    """ Represents the physical board containing blocks in a 2D array
        Extremes row and columns are filled with Wall Blocks.
    """
    def __init__(self, config):
        self.width = int(config["LOGIC"]["board_width"])
        self.height = int(config["LOGIC"]["board_height"])

        self.board = [[None for _ in range(self.width)] for _ in range(self.height)]

        for y in (0, self.height-1):
            for x in range(self.width):
                self.board[y][x] = Block(BlockType.WALL)

        for x in (0, self.width-1):
            for y in range(self.height):
                self.board[y][x] = Block(BlockType.WALL)


    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def put_block(self, x, y, block):
        """
        :param x: 0 <= x < height
        :param y: 0 <= y < width
        :param block : block to be added
        :return:
        """
        self.board[y][x] = block

    def remove_block(self, x, y):
        """
        :param x: 0 <= x < height
        :param y: 0 <= y < width
        :return:
        """
        self.board[y][x] = None

    def get_block(self, x, y):
        """
        :param x: 0 <= x < height
        :param y: 0 <= y < width
        :return:
        """
        return self.board[y][x]

    def get_empty_block_positions(self):
        return [(x,y) for x in range(self.get_width()) for y in range(self.get_height()) if self.get_block(x,y) is None]