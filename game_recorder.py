# Game recording functionality.
import json
from datetime import datetime
import os


class GameRecorder:
    """Handles recording game sessions to file."""

    def __init__(self):
        self._recording = False
        self._game_data = None
        self._recordings_dir = "recordings"
        self._ensure_recordings_directory()

    # Ensure recordings directory exists.
    def _ensure_recordings_directory(self):
        if not os.path.exists(self._recordings_dir):
            os.makedirs(self._recordings_dir)

    # Start recording a new game.
    def start_recording(self, board_size, game_mode, blue_player_type, red_player_type):
        self._recording = True
        self._game_data = {
            "board_size": board_size,
            "game_mode": game_mode,
            "blue_player_type": blue_player_type,
            "red_player_type": red_player_type,
            "moves": [],
            "final_state": {},
        }

    # Record a single move.
    def record_move(self, row, col, letter, player):
        if self._recording and self._game_data is not None:
            self._game_data["moves"].append(
                {"row": row, "col": col, "letter": letter, "player": player}
            )

    # Record final game state.
    def record_final_state(self, winner, blue_score, red_score):
        if self._recording and self._game_data is not None:
            self._game_data["final_state"] = {
                "winner": winner,
                "blue_score": blue_score,
                "red_score": red_score,
            }

    # Save recording to file and stop recording.
    def save_recording(self):
        if not self._recording or self._game_data is None:
            return None

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mode = self._game_data["game_mode"]
        filename = f"game_{mode}_{timestamp}.json"
        filepath = os.path.join(self._recordings_dir, filename)

        # Save to file
        with open(filepath, "w") as f:
            json.dump(self._game_data, f, indent=2)

        self._recording = False
        return filepath

    # Stop recording without saving.
    def cancel_recording(self):
        self._recording = False
        self._game_data = None

    @property
    def is_recording(self):
        return self._recording
