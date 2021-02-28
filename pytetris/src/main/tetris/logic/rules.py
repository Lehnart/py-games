from threading import Lock

from tetris.logic.piece_catalog import PieceCatalog
from tetris.tools.direction import Direction
from tetris.tools.timer import Timer


class Rules:
    DROP_PERIOD = 250
    SCORE_BY_LINE_REMOVED = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}

    def __init__(self, tetris):
        self.tetris = tetris
        self.score = 0

        self.piece_catalog = PieceCatalog()
        self.piece = None
        self.piece_board_positions = None

        self._next_piece()

        self.action_lock = Lock()
        self.drop_timer = Timer(Rules.DROP_PERIOD, self.tetris.move, (Direction.DOWN,))

    def move(self, direction):
        """
        Move the active piece in a direction
        :param direction:
        :return: bool if game over
        """

        with self.action_lock:
            result = self._move_under_lock(direction)
            if not result:
                self.tetris.game_over()

    def rotate(self, rotation):
        """
        rotate the active piece
        :param rotation:
        :return:
        """

        with self.action_lock:
            self._rotate_under_lock(rotation)


    def get_score(self):
        return self.score

    def _move_under_lock(self, direction):
        positions = self.piece_board_positions

        [self._get_board().remove_block(x, y) for x, y in positions]

        next_positions = self._find_next_positions(direction, positions)

        can_it_move = all([self._get_board().is_put_valid(x, y) for x, y in next_positions])

        if can_it_move:
            self._move_piece(next_positions)

        else:
            self._move_piece(positions)

            if direction == Direction.DOWN:
                line_removed_count = self._remove_full_lines()
                self.score += Rules.SCORE_BY_LINE_REMOVED[line_removed_count]
                return self._next_piece()

        return True

    def _remove_full_lines(self):
        return self._get_board().remove_full_lines()

    def _rotate_under_lock(self, rotation):
        positions = self.piece_board_positions
        [self._get_board().remove_block(x, y) for x, y in positions]

        self.piece.rotate(rotation)
        rotate_positions = self.piece.get_element_positions()
        origin_position = (min([p[0] for p in positions]), min(p[1] for p in positions))
        next_positions = []
        for x, y in rotate_positions:
            x, y = (x + origin_position[0], y + origin_position[1])
            next_positions.append((x, y))

        can_it_move = all([self._get_board().is_put_valid(x, y) for x, y in next_positions])

        self._move_piece(next_positions) if can_it_move else self._move_piece(positions)

    def _next_piece(self):
        self.piece = self.piece_catalog.get_random_piece()
        return self._put_piece(self.piece)

    def _move_piece(self, next_positions):
        [self._get_board().put_block(x, y) for x, y in next_positions]
        self.piece_board_positions = [(x, y) for x, y in next_positions]

    def _put_piece(self, piece):
        positions = piece.get_element_positions()
        self.piece_board_positions = []

        x0, y0 = self._get_initial_piece_pos()
        if not all([self._get_board().is_put_valid(x + x0, y + y0) for x, y in positions]):
            return False

        for x, y in positions:
            x, y = (x + self._get_initial_piece_pos()[0], y + self._get_initial_piece_pos()[1])
            self._get_board().put_block(x, y)
            self.piece_board_positions.append((x, y))
        return True

    @staticmethod
    def _find_next_positions(direction, positions):
        next_positions = None
        if direction == Direction.LEFT:
            next_positions = [(x - 1, y) for x, y in positions]
        elif direction == Direction.DOWN:
            next_positions = [(x, y + 1) for x, y in positions]
        elif direction == Direction.RIGHT:
            next_positions = [(x + 1, y) for x, y in positions]
        return next_positions

    def _get_board(self):
        return self.tetris.board

    def _get_initial_piece_pos(self):
        return int((self._get_board().width / 2) - 1), 0

