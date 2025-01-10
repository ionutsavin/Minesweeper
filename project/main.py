import tkinter as tk
from interface.minesweeper_interface import MinesweeperGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperGUI(root)
    root.mainloop()
