# Game logic for SOS game.


class SOSGame:
    EMPTY = ""
    LETTER_S = "S"
    LETTER_O = "O"
    BLUE = "blue"
    RED = "red"
    SIMPLE = "Simple"
    GENERAL = "General"

    # Initialize game with board size and mode.
    def __init__(self, board_size=8):
        if board_size < 3:
            raise ValueError("Board size must be at least 3")

        self._board_size = board_size
        self._board = [
            [self.EMPTY for _ in range(board_size)] for _ in range(board_size)
        ]
        self._current_player = self.BLUE
        self._blue_score = 0
        self._red_score = 0

    @property
    def board_size(self):
        return self._board_size

    @property
    def current_player(self):
        return self._current_player

    @property
    def blue_score(self):
        return self._blue_score

    @property
    def red_score(self):
        return self._red_score

    # Get content of a cell.
    def get_cell(self, row, col):
        if not (0 <= row < self._board_size and 0 <= col < self._board_size):
            raise ValueError(f"Invalid position: ({row}, {col})")
        return self._board[row][col]

    # Place a letter on the board.
    def make_move(self, row, col, letter):
        if not self._is_valid_move(row, col, letter):
            return False

        self._board[row][col] = letter
        self._switch_player()
        return True

    # Check if move is valid.
    def _is_valid_move(self, row, col, letter):
        if not (0 <= row < self._board_size and 0 <= col < self._board_size):
            return False
        if self._board[row][col] != self.EMPTY:
            return False
        if letter not in [self.LETTER_S, self.LETTER_O]:
            return False
        return True

    # Switch to other player.
    def _switch_player(self):
        self._current_player = (
            self.RED if self._current_player == self.BLUE else self.BLUE
        )

    # Detect SOS sequences formed by placing a letter at (row, col)
    def _detect_sos(self, row, col):
        """
        Check all 8 directions from (row, col) for SOS patterns.
        Returns list of SOS sequences found.
        Each sequence is a tuple: ((r1,c1), (r2,c2), (r3,c3))
        """
        sequences = []
        letter = self._board[row][col]

        directions = [
            (0, 1),  # right
            (0, -1),  # left
            (1, 0),  # down
            (-1, 0),  # up
            (1, 1),  # diagonal down-right
            (-1, -1),  # diagonal up-left
            (-1, 1),  # diagonal up-right
            (1, -1),  # diagonal down-left
        ]

        # Check if this S is the start of SOS
        if letter == self.LETTER_S:
            for dr, dc in directions:
                r1, c1 = row + dr, col + dc
                r2, c2 = row + 2 * dr, col + 2 * dc

                if (
                    0 <= r1 < self._board_size
                    and 0 <= c1 < self._board_size
                    and 0 <= r2 < self._board_size
                    and 0 <= c2 < self._board_size
                ):
                    if (
                        self._board[r1][c1] == self.LETTER_O
                        and self._board[r2][c2] == self.LETTER_S
                    ):
                        sequences.append(((row, col), (r1, c1), (r2, c2)))

        # Check if this O is the middle of SOS
        elif letter == self.LETTER_O:
            for dr, dc in directions:
                r_before, c_before = row - dr, col - dc
                r_after, c_after = row + dr, col + dc

                if (
                    0 <= r_before < self._board_size
                    and 0 <= c_before < self._board_size
                    and 0 <= r_after < self._board_size
                    and 0 <= c_after < self._board_size
                ):
                    if (
                        self._board[r_before][c_before] == self.LETTER_S
                        and self._board[r_after][c_after] == self.LETTER_S
                    ):
                        sequences.append(
                            ((r_before, c_before), (row, col), (r_after, c_after))
                        )

        return sequences

    # Reset game with optional new settings
    def reset_game(self, board_size=None):
        if board_size is not None:
            if board_size < 3:
                raise ValueError("Board size must be at least 3")
            self._board_size = board_size

        self._board = [
            [self.EMPTY for _ in range(self._board_size)]
            for _ in range(self._board_size)
        ]
        self._current_player = self.BLUE
        self._blue_score = 0
        self._red_score = 0


# Simple game mode: first SOS wins.
class SimpleGame(SOSGame):
    def __init__(self, board_size=8):
        super().__init__(board_size)

    @property
    def game_mode(self):
        return self.SIMPLE


# General game mode: most SOSs wins.
class GeneralGame(SOSGame):
    def __init__(self, board_size=8):
        super().__init__(board_size)

    @property
    def game_mode(self):
        return self.GENERAL
