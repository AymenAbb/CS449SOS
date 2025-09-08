import tkinter as tk

root = tk.Tk()

root.geometry("500x500")
root.title("Test")

label = tk.Label(root, text="Hello World", font=("Arial", 18))
label.pack()

# lines!
canvas = tk.Canvas(root, width=400, height=120)
canvas.pack()
canvas.create_line(10, 0, 10, 120, fill="black", width=2)  # left line
canvas.create_line(390, 0, 390, 120, fill="black", width=2)  # right line

root.mainloop()
