# GUI for SOS game
import tkinter as tk
from tkinter import messagebox
from SOSGame import SOSGame, SimpleGame, GeneralGame


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

        self.board_frame = tk.Frame(main_frame, bg="white")
        self.board_frame.pack(side=tk.LEFT, padx=10)

        red_frame = tk.Frame(main_frame)
        red_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(
            red_frame, text="Red player", fg="red", font=("Arial", 12, "bold")
        ).pack()
        tk.Radiobutton(red_frame, text="S", variable=self.red_letter, value="S").pack()
        tk.Radiobutton(red_frame, text="O", variable=self.red_letter, value="O").pack()

        # Bottom frame
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10)

        self.turn_label = tk.Label(
            bottom_frame,
            text=f"Current turn: {self.game.current_player}",
            font=("Arial", 12),
        )
        self.turn_label.pack(side=tk.LEFT, padx=20)

        tk.Button(
            bottom_frame, text="New Game", command=self._new_game, font=("Arial", 11)
        ).pack(side=tk.LEFT)

    # Left click
    def _cell_clicked(self, row, col):
        current_player = self.game.current_player

        if current_player == SOSGame.BLUE:
            letter = self.blue_letter.get()
            color = "blue"
        else:
            letter = self.red_letter.get()
            color = "red"

        if self.game.make_move(row, col, letter):
            self.cell_buttons[row][col].config(text=letter, fg=color, state="disabled")
            self.turn_label.config(text=f"Current turn: {self.game.current_player}")
        else:
            if self.game.get_cell(row, col) != SOSGame.EMPTY:
                messagebox.showwarning("Invalid Move", "This cell is already occupied!")

    # Create or recreate the board grid.
    def _create_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.cell_buttons = []
        size = self.game.board_size

        for row in range(size):
            button_row = []
            for col in range(size):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    width=3,
                    height=1,
                    font=("Arial", max(10, 20 - size)),
                    command=lambda r=row, c=col: self._cell_clicked(r, c),
                )
                btn.grid(row=row, column=col, padx=1, pady=1)
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

            # Create appropriate game subclass based on mode
            if game_mode == "Simple":
                self.game = SimpleGame(board_size=board_size)
            else:
                self.game = GeneralGame(board_size=board_size)

            self._create_board()
            self.turn_label.config(text=f"Current turn: {self.game.current_player}")
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter a valid integer for board size!"
            )
