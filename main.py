import tkinter as tk

root = tk.Tk()
root.title("SOS Game")

# Top frame
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

# SOS label
tk.Label(top_frame, text="SOS", font=('Arial', 16, 'bold')).pack(side=tk.LEFT, padx=10)

# Game mode selection
mode = tk.StringVar(value="Simple")
tk.Radiobutton(top_frame, text="Simple game", variable=mode, value="Simple").pack(side=tk.LEFT)
tk.Radiobutton(top_frame, text="General game", variable=mode, value="General").pack(side=tk.LEFT)

# Board size
tk.Label(top_frame, text="Board size").pack(side=tk.LEFT, padx=(20, 5))
board_size_var = tk.StringVar(value='8')
tk.Entry(top_frame, textvariable=board_size_var, width=5).pack(side=tk.LEFT)

# Main frame
main_frame = tk.Frame(root)
main_frame.pack(pady=10)

blue_frame = tk.Frame(main_frame)
blue_frame.pack(side=tk.LEFT, padx=20)
tk.Label(blue_frame, text="Blue player", fg="blue", font=('Arial', 12, 'bold')).pack()
blue_letter = tk.StringVar(value='S')
tk.Radiobutton(blue_frame, text="S", variable=blue_letter, value='S').pack()
tk.Radiobutton(blue_frame, text="O", variable=blue_letter, value='O').pack()

board_frame = tk.Frame(main_frame, bg='lightgray', width=300, height=300)
board_frame.pack(side=tk.LEFT, padx=10)

red_frame = tk.Frame(main_frame)
red_frame.pack(side=tk.LEFT, padx=20)
tk.Label(red_frame, text="Red player", fg="red", font=('Arial', 12, 'bold')).pack()
red_letter = tk.StringVar(value='S')
tk.Radiobutton(red_frame, text="S", variable=red_letter, value='S').pack()
tk.Radiobutton(red_frame, text="O", variable=red_letter, value='O').pack()

# Bottom frame
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

current_turn = "blue"
turn_label = tk.Label(bottom_frame, text=f"Current turn: {current_turn}", font=('Arial', 12))
turn_label.pack(side=tk.LEFT, padx=20)

def new_game():
    print("New game clicked")  # Placeholder for now

tk.Button(bottom_frame, text="New Game", command=new_game, font=('Arial', 11)).pack(side=tk.LEFT)

root.mainloop()