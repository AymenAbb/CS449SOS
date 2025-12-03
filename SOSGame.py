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
    def __init__(self, board_size=8, blue_player=None, red_player=None):
        if board_size < 3:
            raise ValueError("Board size must be at least 3")
        self._board_size = board_size
        self._board = [
            [self.EMPTY for _ in range(board_size)] for _ in range(board_size)
        ]
        self._current_player = self.BLUE
        self._blue_score = 0
        self._red_score = 0
        self._game_over = False
        self._winner = None
        self._sos_lines = []
        self._blue_player = blue_player
        self._red_player = red_player
        self._move_history = []  # NEW: Track move history for recording

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

    @property
    def game_over(self):
        return self._game_over

    @property
    def winner(self):
        return self._winner

    @property
    def sos_lines(self):
        return self._sos_lines

    # NEW: Get move history
    @property
    def move_history(self):
        return self._move_history

    def get_current_player_object(self):
        return (
            self._blue_player if self._current_player == self.BLUE else self._red_player
        )

    # Get content of a cell.
    def get_cell(self, row, col):
        if not (0 <= row < self._board_size and 0 <= col < self._board_size):
            raise ValueError(f"Invalid position: ({row}, {col})")
        return self._board[row][col]

    # Place a letter on the board.
    def make_move(self, row, col, letter):
        if self._game_over:
            return False
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

    # Detect SOS sequences formed by placing a letter at (row, col).
    def _detect_sos(self, row, col):
        letter = self._board[row][col]
        if letter == self.LETTER_S:
            return self._detect_sos_from_s(row, col)
        elif letter == self.LETTER_O:
            return self._detect_sos_from_o(row, col)
        return []

    # Detect SOS sequences where S is at the start.
    def _detect_sos_from_s(self, row, col):
        sequences = []
        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
        ]

        for dr, dc in directions:
            r1, c1 = row + dr, col + dc
            r2, c2 = row + 2 * dr, col + 2 * dc
            if self._is_valid_position(r1, c1) and self._is_valid_position(r2, c2):
                if (
                    self._board[r1][c1] == self.LETTER_O
                    and self._board[r2][c2] == self.LETTER_S
                ):
                    sequences.append(((row, col), (r1, c1), (r2, c2)))
        return sequences

    # Detect SOS sequences where O is in the middle.
    def _detect_sos_from_o(self, row, col):
        sequences = []
        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
        ]

        for dr, dc in directions:
            r_before, c_before = row - dr, col - dc
            r_after, c_after = row + dr, col + dc
            if self._is_valid_position(r_before, c_before) and self._is_valid_position(
                r_after, c_after
            ):
                if (
                    self._board[r_before][c_before] == self.LETTER_S
                    and self._board[r_after][c_after] == self.LETTER_S
                ):
                    sequences.append(
                        ((r_before, c_before), (row, col), (r_after, c_after))
                    )
        return sequences

    # Check if a position is within board boundaries.
    def _is_valid_position(self, row, col):
        return 0 <= row < self._board_size and 0 <= col < self._board_size

    # Check if board is full.
    def _is_board_full(self):
        for row in range(self._board_size):
            for col in range(self._board_size):
                if self._board[row][col] == self.EMPTY:
                    return False
        return True

    # Reset game with optional new settings.
    def reset_game(self, board_size=None, blue_player=None, red_player=None):
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
        self._game_over = False
        self._winner = None
        self._sos_lines = []
        self._move_history = []  # NEW: Clear move history
        if blue_player is not None:
            self._blue_player = blue_player
        if red_player is not None:
            self._red_player = red_player


# Simple game mode: first SOS wins.
class SimpleGame(SOSGame):
    def __init__(self, board_size=8, blue_player=None, red_player=None):
        super().__init__(board_size, blue_player, red_player)

    @property
    def game_mode(self):
        return self.SIMPLE

    # Override make_move for simple game logic.
    def make_move(self, row, col, letter):
        if self._game_over:
            return False
        if not self._is_valid_move(row, col, letter):
            return False

        # Remember current player before switch
        player_before_move = self._current_player

        # Place the letter
        self._board[row][col] = letter

        # NEW: Record move in history
        self._move_history.append(
            {"row": row, "col": col, "letter": letter, "player": player_before_move}
        )

        # Check for SOS
        sos_sequences = self._detect_sos(row, col)

        # First SOS formed - game over, current player wins
        if sos_sequences:
            if player_before_move == self.BLUE:
                self._blue_score += len(sos_sequences)
            else:
                self._red_score += len(sos_sequences)
            for seq in sos_sequences:
                self._sos_lines.append((seq, player_before_move))
            self._game_over = True
            self._winner = player_before_move
        # Board full with no SOS - draw
        elif self._is_board_full():
            self._game_over = True
            self._winner = None
        else:
            self._switch_player()

        return True


# General game mode: most SOSs wins.
class GeneralGame(SOSGame):
    def __init__(self, board_size=8, blue_player=None, red_player=None):
        super().__init__(board_size, blue_player, red_player)

    @property
    def game_mode(self):
        return self.GENERAL

    # Override make_move for general game logic.
    def make_move(self, row, col, letter):
        if self._game_over:
            return False
        if not self._is_valid_move(row, col, letter):
            return False

        # Remember current player before potential switch
        player_before_move = self._current_player

        # Place the letter
        self._board[row][col] = letter

        # NEW: Record move in history
        self._move_history.append(
            {"row": row, "col": col, "letter": letter, "player": player_before_move}
        )

        # Check for SOS
        sos_sequences = self._detect_sos(row, col)

        # SOS formed - add to score, player goes again
        if sos_sequences:
            if player_before_move == self.BLUE:
                self._blue_score += len(sos_sequences)
            else:
                self._red_score += len(sos_sequences)
            for seq in sos_sequences:
                self._sos_lines.append((seq, player_before_move))
            # Don't switch player - they get another turn
        else:
            self._switch_player()

        # Check if board is full
        if self._is_board_full():
            self._game_over = True
            # Determine winner by score
            if self._blue_score > self._red_score:
                self._winner = self.BLUE
            elif self._red_score > self._blue_score:
                self._winner = self.RED
            else:
                self._winner = None

        return True
