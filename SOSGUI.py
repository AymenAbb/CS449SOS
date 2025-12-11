import tkinter as tk
from tkinter import messagebox, filedialog
from SOSGame import SOSGame, SimpleGame, GeneralGame
from player import HumanPlayer, ComputerPlayer
from game_recorder import GameRecorder
from game_replayer import GameReplayer
from llm_player import LLMPlayer

# UI configuration constants
COMPUTER_MOVE_DELAY_MS = 5000
REPLAY_SPEED_MS = 500
MIN_CELL_SIZE = 40
BOARD_PIXEL_BUDGET = 400


class SOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")

        # Initialize game
        self.game = SimpleGame()
        self.blue_letter = tk.StringVar(value="S")
        self.red_letter = tk.StringVar(value="S")
        self.board_size_var = tk.StringVar(value="8")
        self.mode = tk.StringVar(value="Simple")
        self.blue_player_type = tk.StringVar(value="Human")
        self.red_player_type = tk.StringVar(value="Human")

        # Recording and replay
        self.record_var = tk.BooleanVar(value=False)
        self.recorder = GameRecorder()
        self.replayer = GameReplayer()
        self.replay_mode = False
        self.replay_speed = REPLAY_SPEED_MS

        self._create_widgets()
        self._create_board()

    def _create_widgets(self):
        self._create_top_frame()
        self._create_main_frame()
        self._create_bottom_frame()

    # Create top frame with game mode and board size controls.
    def _create_top_frame(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # SOS label
        tk.Label(top_frame, text="SOS", font=("Arial", 16, "bold")).pack(
            side=tk.LEFT, padx=10
        )

        # Game mode selection
        tk.Radiobutton(
            top_frame, text="Simple game", variable=self.mode, value="Simple"
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            top_frame, text="General game", variable=self.mode, value="General"
        ).pack(side=tk.LEFT)

        # Board size
        tk.Label(top_frame, text="Board size").pack(side=tk.LEFT, padx=(20, 5))
        tk.Entry(top_frame, textvariable=self.board_size_var, width=5).pack(
            side=tk.LEFT
        )

    # Create main frame with player controls and board.
    def _create_main_frame(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)

        # Blue player frame
        self.blue_score_label = self._create_player_frame(
            main_frame, "Blue player", "blue", self.blue_letter, self.blue_player_type
        )

        # Board frame
        self.board_frame = tk.Frame(main_frame)
        self.board_frame.pack(side=tk.LEFT, padx=10)

        # Red player frame
        self.red_score_label = self._create_player_frame(
            main_frame, "Red player", "red", self.red_letter, self.red_player_type
        )

    # Create a player frame with letter and player type controls.
    def _create_player_frame(
        self, parent, label_text, color, letter_var, player_type_var
    ):
        frame = tk.Frame(parent)
        frame.pack(side=tk.LEFT, padx=20)

        tk.Label(frame, text=label_text, fg=color, font=("Arial", 12, "bold")).pack()

        tk.Radiobutton(frame, text="S", variable=letter_var, value="S").pack()
        tk.Radiobutton(frame, text="O", variable=letter_var, value="O").pack()

        tk.Radiobutton(
            frame, text="Human", variable=player_type_var, value="Human"
        ).pack()
        tk.Radiobutton(
            frame, text="Computer", variable=player_type_var, value="Computer"
        ).pack()
        tk.Radiobutton(frame, text="LLM", variable=player_type_var, value="LLM").pack()

        # Score label
        score_label = tk.Label(frame, text="Score: 0", font=("Arial", 10))
        score_label.pack(pady=(10, 0))

        # Add Replay button to red player frame
        if color == "red":
            tk.Button(
                frame, text="Replay", command=self._start_replay, font=("Arial", 10)
            ).pack(pady=(10, 0))

        return score_label

    # Create bottom frame with turn label and buttons.
    def _create_bottom_frame(self):
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10)

        # Record game checkbox
        tk.Checkbutton(bottom_frame, text="Record game", variable=self.record_var).pack(
            side=tk.LEFT, padx=10
        )

        # Current turn label
        self.turn_label = tk.Label(
            bottom_frame,
            text=f"Current turn: {self.game.current_player}",
            font=("Arial", 12),
        )
        self.turn_label.pack(side=tk.LEFT, padx=20)

        # New Game button
        tk.Button(
            bottom_frame, text="New Game", command=self._new_game, font=("Arial", 11)
        ).pack(side=tk.LEFT)

    # Handle cell click during normal gameplay.
    def _cell_clicked(self, row, col):
        if self.game.game_over or self.replay_mode:
            return

        player = self.game.get_current_player_object()
        if isinstance(player, (ComputerPlayer, LLMPlayer)):
            return

        # Capture the player BEFORE the move
        player_making_move = self.game.current_player
        if player_making_move == SOSGame.BLUE:
            letter = self.blue_letter.get()
            color = "blue"
        else:
            letter = self.red_letter.get()
            color = "red"

        # Attempt to make the move
        if self.game.make_move(row, col, letter):
            # Record move if recording is enabled
            if self.record_var.get() and self.recorder.is_recording:
                self.recorder.record_move(row, col, letter, player_making_move)

            # Set button text in the color of the player who MADE the move
            self.cell_buttons[row][col].config(
                text=letter, fg=color, disabledforeground=color, state="disabled"
            )

            # Draw SOS lines
            self._draw_sos_lines()

            # Update scores
            self._update_scores()

            # Update turn label
            if not self.game.game_over:
                self.turn_label.config(text=f"Current turn: {self.game.current_player}")
                self._check_computer_turn()
            else:
                self._show_game_over()
        else:
            if self.game.get_cell(row, col) != SOSGame.EMPTY:
                messagebox.showwarning("Invalid Move", "This cell is already occupied!")

    def _check_computer_turn(self):
        if not self.game.game_over and not self.replay_mode:
            player = self.game.get_current_player_object()
            if isinstance(player, (ComputerPlayer, LLMPlayer)):
                self.root.after(COMPUTER_MOVE_DELAY_MS, self._make_computer_move)

    def _make_computer_move(self):
        if self.replay_mode:
            return
        player = self.game.get_current_player_object()
        if isinstance(player, (ComputerPlayer, LLMPlayer)):
            move = player.get_move(self.game)
            if move:
                row, col, letter = move
                color = "blue" if self.game.current_player == SOSGame.BLUE else "red"
                player_making_move = self.game.current_player

                if self.game.make_move(row, col, letter):
                    # Record move if recording is enabled
                    if self.record_var.get() and self.recorder.is_recording:
                        self.recorder.record_move(row, col, letter, player_making_move)

                    self.cell_buttons[row][col].config(
                        text=letter,
                        fg=color,
                        disabledforeground=color,
                        state="disabled",
                    )
                    self._draw_sos_lines()
                    self._update_scores()

                    if not self.game.game_over:
                        self.turn_label.config(
                            text=f"Current turn: {self.game.current_player}"
                        )
                        self._check_computer_turn()
                    else:
                        self._show_game_over()

    # Draw lines through SOS sequences
    def _draw_sos_lines(self):
        # Clear existing lines
        self.canvas.delete("sos_line")

        for line_data in self.game.sos_lines:
            seq, player = line_data
            start_cell, mid_cell, end_cell = seq

            # Calculate center coordinates
            start_row, start_col = start_cell
            end_row, end_col = end_cell
            cell_size = self.cell_size

            x1 = start_col * cell_size + cell_size // 2
            y1 = start_row * cell_size + cell_size // 2
            x2 = end_col * cell_size + cell_size // 2
            y2 = end_row * cell_size + cell_size // 2

            color = "blue" if player == SOSGame.BLUE else "red"
            self.canvas.create_line(
                x1, y1, x2, y2, fill=color, width=3, tags="sos_line"
            )

    # Update score labels
    def _update_scores(self):
        self.blue_score_label.config(text=f"Score: {self.game.blue_score}")
        self.red_score_label.config(text=f"Score: {self.game.red_score}")

    # Show game over message
    def _show_game_over(self):
        # Save recording if enabled
        if self.record_var.get() and self.recorder.is_recording:
            self.recorder.record_final_state(
                self.game.winner, self.game.blue_score, self.game.red_score
            )
            filepath = self.recorder.save_recording()
            if filepath:
                messagebox.showinfo("Recording Saved", f"Game recorded to:\n{filepath}")

        if self.game.winner is None:
            message = "Game Over! It's a draw!"
            self.turn_label.config(text="Game Over: Draw")
        elif self.game.winner == SOSGame.BLUE:
            message = f"Game Over! Blue wins with {self.game.blue_score} SOS!"
            self.turn_label.config(text="Game Over: Blue wins!")
        else:
            message = f"Game Over! Red wins with {self.game.red_score} SOS!"
            self.turn_label.config(text="Game Over: Red wins!")

        messagebox.showinfo("Game Over", message)

    # Create or recreate the board grid.
    def _create_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        size = self.game.board_size
        self.cell_size = max(MIN_CELL_SIZE, BOARD_PIXEL_BUDGET // size)

        # Create canvas for drawing lines
        canvas_size = size * self.cell_size
        self.canvas = tk.Canvas(
            self.board_frame, width=canvas_size, height=canvas_size, bg="white"
        )
        self.canvas.pack()

        self.cell_buttons = []
        for row in range(size):
            button_row = []
            for col in range(size):
                x = col * self.cell_size
                y = row * self.cell_size

                # Create button on canvas
                btn = tk.Button(
                    self.canvas,
                    text="",
                    width=3,
                    height=1,
                    font=("Arial", max(10, 20 - size)),
                    command=lambda r=row, c=col: self._cell_clicked(r, c),
                )
                self.canvas.create_window(
                    x + self.cell_size // 2, y + self.cell_size // 2, window=btn
                )
                button_row.append(btn)
            self.cell_buttons.append(button_row)

    # Start new game with current settings.
    def _new_game(self):
        try:
            # Stop replay mode if active
            self.replay_mode = False

            board_size = int(self.board_size_var.get())
            if board_size < 3:
                messagebox.showerror(
                    "Invalid Board Size", "Board size must be at least 3!"
                )
                return

            game_mode = self.mode.get()

            if self.blue_player_type.get() == "Human":
                blue_player = HumanPlayer("blue")
            elif self.blue_player_type.get() == "LLM":
                blue_player = LLMPlayer("blue")
            else:
                blue_player = ComputerPlayer("blue")

            if self.red_player_type.get() == "Human":
                red_player = HumanPlayer("red")
            elif self.red_player_type.get() == "LLM":
                red_player = LLMPlayer("red")
            else:
                red_player = ComputerPlayer("red")

            # Create appropriate game subclass based on mode
            if game_mode == "Simple":
                self.game = SimpleGame(
                    board_size=board_size,
                    blue_player=blue_player,
                    red_player=red_player,
                )
            else:
                self.game = GeneralGame(
                    board_size=board_size,
                    blue_player=blue_player,
                    red_player=red_player,
                )

            # Start recording if checkbox is checked
            if self.record_var.get():
                self.recorder.start_recording(
                    board_size,
                    game_mode,
                    self.blue_player_type.get(),
                    self.red_player_type.get(),
                )

            self._create_board()
            self.turn_label.config(text=f"Current turn: {self.game.current_player}")
            self._update_scores()
            self._check_computer_turn()

        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter a valid integer for board size!"
            )

    # Start replay from file.
    def _start_replay(self):
        filepath = filedialog.askopenfilename(
            title="Select Recording to Replay",
            initialdir="recordings",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )

        if not filepath:
            return

        try:
            # Load the recording
            self.replayer.load_game(filepath)
            config = self.replayer.get_game_config()

            # Set up game with recording configuration
            self.board_size_var.set(str(config["board_size"]))
            self.mode.set(config["game_mode"])
            self.blue_player_type.set(config["blue_player_type"])
            self.red_player_type.set(config["red_player_type"])

            # Disable recording during replay
            self.record_var.set(False)

            # Create game
            blue_player = HumanPlayer("blue")
            red_player = HumanPlayer("red")

            if config["game_mode"] == "Simple":
                self.game = SimpleGame(
                    board_size=config["board_size"],
                    blue_player=blue_player,
                    red_player=red_player,
                )
            else:
                self.game = GeneralGame(
                    board_size=config["board_size"],
                    blue_player=blue_player,
                    red_player=red_player,
                )

            # Reset board
            self._create_board()
            self.turn_label.config(text="Replay Mode")
            self._update_scores()

            # Start replay mode
            self.replay_mode = True
            self._replay_next_move()

        except Exception as e:
            messagebox.showerror("Replay Error", f"Failed to load recording:\n{str(e)}")

    # Replay next move in sequence.
    def _replay_next_move(self):
        if not self.replay_mode:
            return

        if not self.replayer.has_next_move():
            # Replay finished
            self.replay_mode = False
            self.turn_label.config(text="Replay Complete")

            # Show final state
            final_state = self.replayer.get_final_state()
            if final_state["winner"] is None:
                message = "Replay Complete! It was a draw!"
            elif final_state["winner"] == SOSGame.BLUE:
                message = (
                    f"Replay Complete! Blue won with {final_state['blue_score']} SOS!"
                )
            else:
                message = (
                    f"Replay Complete! Red won with {final_state['red_score']} SOS!"
                )

            messagebox.showinfo("Replay Complete", message)
            return

        # Get next move
        move = self.replayer.get_next_move()
        row = move["row"]
        col = move["col"]
        letter = move["letter"]
        player = move["player"]

        # Execute move
        self.game.make_move(row, col, letter)

        # Update UI
        color = "blue" if player == SOSGame.BLUE else "red"
        self.cell_buttons[row][col].config(
            text=letter, fg=color, disabledforeground=color, state="disabled"
        )

        self._draw_sos_lines()
        self._update_scores()
        self.turn_label.config(
            text=f"Replay Mode - Move {self.replayer.get_current_move_index()}/{self.replayer.get_total_moves()}"
        )

        # Schedule next move
        self.root.after(self.replay_speed, self._replay_next_move)
