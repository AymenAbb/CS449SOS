# LLM-powered opponent using Google Gemini.
import os
import re
import google.generativeai as genai
from player import Player
import random


class LLMPlayer(Player):
    def __init__(self, color):
        super().__init__(color)
        # Get API key from environment variable
        self.api_key = os.getenv("GEMINI_API_KEY")

        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Use gemini-1.5-flash for speed
            self.model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not set. LLMPlayer will use random moves.")

    def get_move(self, game):
        if not self.model:
            raise RuntimeError("GEMINI_API_KEY not set")

        try:
            prompt = self._build_prompt(game)
            response = self.model.generate_content(prompt)
            content = response.text.strip()

            # Print what the LLM is thinking
            print(f"\n[LLM {self.color}] Response: {content}\n")

            move = self._parse_move(content, game)
            print(f"[LLM {self.color}] Parsed move: {move}")

            if move:
                row, col, letter = move
                # Debug: Check what's at that position
                current = game.get_cell(row, col)
                print(
                    f"[LLM {self.color}] Cell at [{row}][{col}] contains: '{current}'"
                )
                print(f"[LLM {self.color}] game.EMPTY = '{game.EMPTY}'")
                print(f"[LLM {self.color}] Is empty? {current == game.EMPTY}")
                print(f"[LLM {self.color}] Is valid? {self._is_valid_move(move, game)}")

            if move and self._is_valid_move(move, game):
                print(
                    f"[LLM {self.color}] Playing: row={move[0]}, col={move[1]}, letter={move[2]}"
                )
                return move
            else:
                raise ValueError(f"LLM returned invalid move: {content}")

        except Exception as e:
            # Show errors
            print(f"\n{'='*60}")
            print(f"[LLM {self.color}] FAILED!")
            print(f"Error: {e}")
            print(f"{'='*60}\n")
            raise

    def _build_prompt(self, game):
        # Prompt
        board_str = self._format_board(game)

        # Analyze board
        empty_count = sum(
            1
            for r in range(game.board_size)
            for c in range(game.board_size)
            if game.get_cell(r, c) == game.EMPTY
        )
        game_phase = (
            "early"
            if empty_count > game.board_size * game.board_size * 0.7
            else (
                "mid"
                if empty_count > game.board_size * game.board_size * 0.3
                else "late"
            )
        )

        prompt = f"""You are an expert SOS player. You are {self.color} player.

        GAME RULES:
        - Goal: Create S-O-S sequences in straight lines (horizontal, vertical, diagonal)
        - {'Simple mode: First player to make an SOS wins immediately' if game.game_mode == 'Simple' else 'General mode: Make the most SOS sequences by game end'}

        CURRENT STATE:
        Board: {game.board_size}x{game.board_size} | Phase: {game_phase} game
        Scores: Blue={game.blue_score}, Red={game.red_score}
        You are: {self.color}

        BOARD (. = empty):
        {board_str}

        WINNING STRATEGY:
        1. ATTACK: Scan for 2-letter partial sequences (S-O or O-S) where you can complete the SOS
        - Check all 8 directions from every cell
        - Example: If you see "S O .", place S at position 2
   
        2. DEFEND: Block opponent's winning moves
        - Look for their partial sequences
        - Place your letter to prevent their completion
   
        3. SETUP: Create multiple threats
        - Place letters that create future SOS opportunities
        - In middle game, position Os between Ss for multi-directional scoring

        4. PATTERN RECOGNITION:
        - "S . S" → place O in middle for instant SOS
        - ". O S" or "S O ." → place S to complete
        - Diagonal patterns are harder to spot - check carefully!

        RESPONSE: Output ONLY: row,col,letter
        Example: 2,3,O

        Analyze the board carefully. Your move:"""
        return prompt

    def _format_board(self, game):
        # Format board as text grid with coordinates.
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
        match = re.search(r"(\d+)\s*,\s*(\d+)\s*,\s*([SOso])", response)
        if match:
            row = int(match.group(1))
            col = int(match.group(2))
            letter = match.group(3).upper()
            return (row, col, letter)
        return None

    def _is_valid_move(self, move, game):
        if not move:
            return False
        row, col, letter = move

        # Check bounds
        if not (0 <= row < game.board_size and 0 <= col < game.board_size):
            return False

        # Check cell is empty
        if game.get_cell(row, col) != game.EMPTY:
            return False

        # Check letter is valid
        if letter not in ["S", "O"]:
            return False

        return True

    """
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
    """
