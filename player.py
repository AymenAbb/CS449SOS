# Player class hierarchy for computer opponent
import random
from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

    @abstractmethod
    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def get_move(self, game):
        return None


class ComputerPlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def get_move(self, game):
        # Try to find a winning/blocking SOS move first
        move = self._find_sos_move(game)
        if move:
            return move
        return self._random_move(game)

    # Find any move that creates an SOS.
    def _find_sos_move(self, game):
        for row in range(game.board_size):
            for col in range(game.board_size):
                if game.get_cell(row, col) == game.EMPTY:
                    if self._creates_sos(game, row, col, "S"):
                        return (row, col, "S")
                    if self._creates_sos(game, row, col, "O"):
                        return (row, col, "O")
        return None

    def _creates_sos(self, game, row, col, letter):
        original = game._board[row][col]
        game._board[row][col] = letter
        sequences = game._detect_sos(row, col)
        game._board[row][col] = original
        return len(sequences) > 0

    def _random_move(self, game):
        valid_moves = []
        for row in range(game.board_size):
            for col in range(game.board_size):
                if game.get_cell(row, col) == game.EMPTY:
                    valid_moves.append((row, col))
        if valid_moves:
            row, col = random.choice(valid_moves)
            letter = random.choice(["S", "O"])
            return (row, col, letter)
        return None
