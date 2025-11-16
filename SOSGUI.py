import tkinter as tk
from tkinter import messagebox
from SOSGame import SOSGame, SimpleGame, GeneralGame
from player import HumanPlayer, ComputerPlayer


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

        self._create_widgets()
        self._create_board()

    def _create_widgets(self):
        # Top frame
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

        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)

        # Blue player frame
        blue_frame = tk.Frame(main_frame)
        blue_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(
            blue_frame, text="Blue player", fg="blue", font=("Arial", 12, "bold")
        ).pack()
        tk.Radiobutton(
            blue_frame, text="S", variable=self.blue_letter, value="S"
        ).pack()
        tk.Radiobutton(
            blue_frame, text="O", variable=self.blue_letter, value="O"
        ).pack()
        tk.Radiobutton(
            blue_frame, text="Human", variable=self.blue_player_type, value="Human"
        ).pack()
        tk.Radiobutton(
            blue_frame,
            text="Computer",
            variable=self.blue_player_type,
            value="Computer",
        ).pack()

        # Blue score label
        self.blue_score_label = tk.Label(
            blue_frame, text="Score: 0", font=("Arial", 10)
        )
        self.blue_score_label.pack(pady=(10, 0))

        # Board frame with canvas
        self.board_frame = tk.Frame(main_frame)
        self.board_frame.pack(side=tk.LEFT, padx=10)

        # Red player frame
        red_frame = tk.Frame(main_frame)
        red_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(
            red_frame, text="Red player", fg="red", font=("Arial", 12, "bold")
        ).pack()
        tk.Radiobutton(red_frame, text="S", variable=self.red_letter, value="S").pack()
        tk.Radiobutton(red_frame, text="O", variable=self.red_letter, value="O").pack()
        tk.Radiobutton(
            red_frame, text="Human", variable=self.red_player_type, value="Human"
        ).pack()
        tk.Radiobutton(
            red_frame, text="Computer", variable=self.red_player_type, value="Computer"
        ).pack()

        # Red score label
        self.red_score_label = tk.Label(red_frame, text="Score: 0", font=("Arial", 10))
        self.red_score_label.pack(pady=(10, 0))

        # Bottom frame
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10)

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

    # Left click
    def _cell_clicked(self, row, col):
        if self.game.game_over:
            return

        player = self.game.get_current_player_object()
        if isinstance(player, ComputerPlayer):
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
        if not self.game.game_over:
            player = self.game.get_current_player_object()
            if isinstance(player, ComputerPlayer):
                self.root.after(500, self._make_computer_move)

    def _make_computer_move(self):
        player = self.game.get_current_player_object()

        if isinstance(player, ComputerPlayer):
            move = player.get_move(self.game)
            if move:
                row, col, letter = move
                color = "blue" if self.game.current_player == SOSGame.BLUE else "red"

                if self.game.make_move(row, col, letter):
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
        self.cell_size = max(40, 400 // size)

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
            board_size = int(self.board_size_var.get())
            if board_size < 3:
                messagebox.showerror(
                    "Invalid Board Size", "Board size must be at least 3!"
                )
                return

            game_mode = self.mode.get()

            blue_player = (
                HumanPlayer("blue")
                if self.blue_player_type.get() == "Human"
                else ComputerPlayer("blue")
            )
            red_player = (
                HumanPlayer("red")
                if self.red_player_type.get() == "Human"
                else ComputerPlayer("red")
            )

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

            self._create_board()
            self.turn_label.config(text=f"Current turn: {self.game.current_player}")
            self._update_scores()
            self._check_computer_turn()
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter a valid integer for board size!"
            )
