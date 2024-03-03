import tkinter as tk
from app.gui import GUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Real-Time Template Matching")

    gui = GUI(root)

    root.mainloop()
