# Game logic for SOS game.
class SOSGame: 
    
    EMPTY = ''
    LETTER_S = 'S'
    LETTER_O = 'O'
    BLUE = 'blue'
    RED = 'red'
    SIMPLE = 'Simple'
    GENERAL = 'General'
    
    # Initialize game with board size and mode.
    def __init__(self, board_size=8, game_mode=SIMPLE):  
        if board_size < 3:
            raise ValueError("Board size must be at least 3")
        
        self._board_size = board_size
        self._game_mode = game_mode
        self._board = [[self.EMPTY for _ in range(board_size)] 
                       for _ in range(board_size)]
        self._current_player = self.BLUE
    
    @property
    def board_size(self):
        return self._board_size
    
    @property
    def game_mode(self):
        return self._game_mode
    
    @property
    def current_player(self):
        return self._current_player
    
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
        self._current_player = self.RED if self._current_player == self.BLUE else self.BLUE