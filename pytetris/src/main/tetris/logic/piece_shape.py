class PieceShape:
    """ Represents the shape of blocks that will be added to the board.
        It contains also the rotated shapes.
    """

    def __init__(self, shape_strs):
        """
        :param shapes: 2D array of string with each rotated piece. Each element of 1st dim represent a row of the piece.
        Each element of 2nd dim is a different rotation of the piece
        Each element of 3rd dim is the shape of the piece. x = block, o = no block.
        """

        self.piece_shapes = self._convert_input(shape_strs)

    def get_element_positions(self, rotation_index):
        """
        Get the bool array representing the shape
        :param rotation_index: index between 0 and 3 representing the rotation state of the shape
        :return: 2D array of booleans
        """
        return self.piece_shapes[rotation_index]

    def _convert_input(self, shape_strs):
        piece_shape_strs = self._format_strs(shape_strs)
        return self._transform_strs(piece_shape_strs)

    def _format_strs(self, shape_strs):
        piece_shape_strs = ["", "", "", ""]
        for row_strs in shape_strs:
            for index, row_str in enumerate(row_strs):
                piece_shape_strs[index] += row_str + '\n'
        return piece_shape_strs

    def _transform_strs(self, piece_shape_strs):
        piece_shapes = []
        for piece_shape_str in piece_shape_strs:
            piece_shape = self._transform_str(piece_shape_str)
            piece_shapes.append(piece_shape)
        return piece_shapes

    def _transform_str(self, piece_shape_str):
        piece_shape = [[]]
        for i, char in enumerate(piece_shape_str):
            if char == 'x':
                piece_shape[-1].append(True)
            if char == 'o':
                piece_shape[-1].append(False)
            if char == '\n' and i != len(piece_shape_str) - 1:
                piece_shape.append([])
        return piece_shape
