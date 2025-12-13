# LLM-powered opponent using local LM Studio server
import requests
import re
from player import Player


class LLMPlayer(Player):
    def __init__(self, color):
        super().__init__(color)
        # LM Studio local server URL
        self.api_url = "http://localhost:1234/v1/chat/completions"
        self.model = "local-model"

    def get_move(self, game):
        max_retries = 5
        current_prompt = self._build_prompt(game)

        print(f"\n[LLM {self.color}] Thinking locally...")

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a master SOS player. Return ONLY the move: row,col,letter. No explanation.",
                            },
                            {"role": "user", "content": current_prompt},
                        ],
                        "temperature": 0.0,
                        "max_tokens": 50,
                    },
                    timeout=30,
                )

                if response.status_code != 200:
                    print(f"[LLM {self.color}] Server Error: {response.text}")
                    continue

                content = response.json()["choices"][0]["message"]["content"].strip()
                print(f"[LLM {self.color}] Response (Attempt {attempt+1}): {content}")

                move = self._parse_move(content, game)

                # VALIDATION
                if move:
                    if self._is_valid_move(move, game):
                        row, col, letter = move
                        print(
                            f"[LLM {self.color}] Playing: row={row}, col={col}, letter={letter}"
                        )
                        return move
                    else:
                        print(
                            f"[LLM {self.color}] Invalid logic: {content} (Cell occupied or out of bounds)"
                        )
                        # Add error to prompt so it learns
                        current_prompt += f"\n\nERROR: Move {content} is invalid! Cell is occupied or out of bounds. Choose an EMPTY '.' cell."
                else:
                    print(f"[LLM {self.color}] Format error: {content}")
                    current_prompt += f"\n\nERROR: Invalid format. Output ONLY: row,col,letter (e.g. 2,3,S)"

            except Exception as e:
                print(f"[LLM {self.color}] Connection Error: {e}")

        # Failed 11 times
        raise RuntimeError(
            f"LLM failed to make a valid move after {max_retries} attempts!"
        )

    def _build_prompt(self, game):
        board_str = self._format_board(game)

        prompt = f"""You are a master SOS player. You are {self.color}.
Your goal is to BEAT the opponent by forming 'S-O-S' sequences.

CURRENT BOARD:
{board_str}

CRITICAL INSTRUCTIONS:
1. IMMEDIATE WIN: Look for 'S-O-.' or '. -O-S' or 'S-.-S' (horizontally, vertically, diagonal). If found, FILL IT to score!
2. BLOCK OPPONENT: If the opponent has 2/3 of an SOS (e.g. 'S-O-.'), you MUST block it!
3. DON'T SET UP LOSES: Do NOT place an 'O' next to an 'S' unless you are completing a sequence.
4. AGGRESSIVE PLAY: If no immediate win, place 'S' far away from other letters to start new threats.

Output ONLY the move: row,col,letter
Example: 1,2,S

Analyze every row, column, and diagonal. Your move:"""
        return prompt

    def _format_board(self, game):
        lines = []
        lines.append("   " + " ".join(str(i) for i in range(game.board_size)))

        # Rows with row numbers
        for row in range(game.board_size):
            row_str = f"{row} |"
            for col in range(game.board_size):
                cell = game.get_cell(row, col)
                char = cell if cell != game.EMPTY else "."
                row_str += f" {char}"
            lines.append(row_str)

        return "\n".join(lines)

    def _parse_move(self, response, game):
        # Parse LLM response into (row, col, letter) tuple
        # Extract pattern like "2,3,S" or "2, 3, S"
        matches = list(re.finditer(r"(\d+)\s*,\s*(\d+)\s*,\s*([SOso])", response))
        if matches:
            match = matches[-1]  # Take the last one found
            row = int(match.group(1))
            col = int(match.group(2))
            letter = match.group(3).upper()
            return (row, col, letter)
        return None

    def _is_valid_move(self, move, game):
        if not move:
            return False
        row, col, letter = move

        if not (0 <= row < game.board_size and 0 <= col < game.board_size):
            return False

        if game.get_cell(row, col) != game.EMPTY:
            return False

        if letter not in ["S", "O"]:
            return False

        return True
