# Game replay functionality.

import json
import os


# Handles loading and replaying recorded games
class GameReplayer:
    def __init__(self):
        self._game_data = None
        self._current_move_index = 0

    # Load game from file
    def load_game(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Recording file not found: {filepath}")

        with open(filepath, "r") as f:
            self._game_data = json.load(f)

        self._current_move_index = 0
        self._validate_game_data()

    # Validate loaded game data structure
    def _validate_game_data(self):
        required_keys = [
            "board_size",
            "game_mode",
            "blue_player_type",
            "red_player_type",
            "moves",
            "final_state",
        ]
        for key in required_keys:
            if key not in self._game_data:
                raise ValueError(f"Invalid recording file: missing '{key}'")

    # Get game configuration
    def get_game_config(self):
        if self._game_data is None:
            return None

        return {
            "board_size": self._game_data["board_size"],
            "game_mode": self._game_data["game_mode"],
            "blue_player_type": self._game_data["blue_player_type"],
            "red_player_type": self._game_data["red_player_type"],
        }

    # Get next move in sequence
    def get_next_move(self):
        if self._game_data is None:
            return None

        if self._current_move_index >= len(self._game_data["moves"]):
            return None

        move = self._game_data["moves"][self._current_move_index]
        self._current_move_index += 1
        return move

    # Reset to beginning of replay
    def reset(self):
        self._current_move_index = 0

    # Check if there are more moves
    def has_next_move(self):
        if self._game_data is None:
            return False
        return self._current_move_index < len(self._game_data["moves"])

    # Get total number of moves
    def get_total_moves(self):
        if self._game_data is None:
            return 0
        return len(self._game_data["moves"])

    # Get current move index
    def get_current_move_index(self):
        return self._current_move_index

    # Get final game state
    def get_final_state(self):
        if self._game_data is None:
            return None
        return self._game_data["final_state"]
