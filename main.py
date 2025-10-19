import tkinter as tk

root = tk.Tk()
root.title("SOS Game")

# Top frame for game settings
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

root.mainloop()