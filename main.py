import tkinter as tk

root = tk.Tk()

root.geometry("500x500")
root.title("Test")

label = tk.Label(root, text="Hello World", font=("Arial", 18))
label.pack()

root.mainloop()
