import tkinter as tk

root = tk.Tk()

root.geometry("500x500")
root.title("Test")

label = tk.Label(root, text="Hello World", font=("Arial", 18))
label.pack()

# lines!
canvas = tk.Canvas(root, width=400, height=120)
canvas.pack()
canvas.create_line(10, 60, 390, 60, fill="red", width=2)

root.mainloop()
