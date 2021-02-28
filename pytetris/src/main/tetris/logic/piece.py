from tetris.tools.rotation import Rotation


class Piece:
    """ Represents a tetris piece with a shape and its state"""

    def __init__(self, shape):
        self.shape = shape
        self.rotation_index = 0

    def get_element_positions(self):
        """
        Get array of (x,y) representing the element positions
        :return: array of x and y positions
        """
        bools = self.shape.get_element_positions(self.rotation_index)
        positions = [(x, y) for y in range(len(bools)) for x in range(len(bools[y])) if bools[y][x] ]
        return positions

    def rotate(self, rotation):
        if rotation == Rotation.CLOCKWISE :
            self.rotation_index = (self.rotation_index + 1) % 4
        elif rotation == Rotation.COUNTER_CLOCKWISE:
            self.rotation_index = (self.rotation_index - 1) % 4

