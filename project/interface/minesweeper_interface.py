import tkinter as tk
from tkinter import messagebox
from gamelogic.minesweeper_logic import MinesweeperLogic


class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.configure(bg="#2c2c2c")  # dark gray

        self.start_frame = None
        self.rows_entry = None
        self.cols_entry = None
        self.bombs_entry = None
        self.start_button = None

        self.board_frame = None
        self.buttons = None
        self.game = None
        self.rows = 0
        self.cols = 0
        self.bombs = 0

        self.timer_label = None
        self.remaining_time = 0
        self.timer_id = None

        self.setup_startup_window()

    def setup_startup_window(self):
        self.start_frame = tk.Frame(self.root, bg="#2c2c2c", padx=20, pady=20)
        self.start_frame.pack(expand=True)
        self.create_startup_inputs()
        self.create_start_button()

    def create_startup_inputs(self):
        tk.Label(self.start_frame, text="Rows:", font=("Arial", 12), fg="white", bg="#2c2c2c").grid(row=0, column=0,
                                                                                                    padx=10, pady=5)
        self.rows_entry = tk.Entry(self.start_frame, width=5)
        self.rows_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.start_frame, text="Columns:", font=("Arial", 12), fg="white", bg="#2c2c2c").grid(row=0, column=2,
                                                                                                       padx=10, pady=5)
        self.cols_entry = tk.Entry(self.start_frame, width=5)
        self.cols_entry.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(self.start_frame, text="Bombs:", font=("Arial", 12), fg="white", bg="#2c2c2c").grid(row=0, column=4,
                                                                                                     padx=10, pady=5)
        self.bombs_entry = tk.Entry(self.start_frame, width=5)
        self.bombs_entry.grid(row=0, column=5, padx=10, pady=5)

    def create_start_button(self):
        self.start_button = tk.Button(
            self.start_frame,
            text="Start Game",
            font=("Arial", 12),
            bg="red",
            fg="black",
            command=self.start_game
        )
        self.start_button.grid(row=1, column=0, columnspan=6, pady=20)

    def start_game(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            bombs = int(self.bombs_entry.get())
            max_rows = 20
            max_cols = 30
            if rows <= 0 or cols <= 0:
                raise ValueError("Number of rows and columns must be positive.")
            if rows > max_rows or cols > max_cols:
                raise ValueError(f"Number of rows and columns cannot exceed {max_rows}.")
            if bombs <= 0:
                raise ValueError("Number of bombs must be greater than zero.")
            if bombs >= rows * cols / 2:
                raise ValueError("There are too many bombs for this configuration.")
            if bombs < 2:
                raise ValueError("There must be at least 2 bombs.")
            self.rows = rows
            self.cols = cols
            self.bombs = bombs
            self.start_frame.destroy()
            self.setup_game_board()

            self.remaining_time = rows * cols + bombs
            self.create_timer()
            self.update_timer()

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def create_timer(self):
        self.timer_label = tk.Label(self.root, font=("Arial", 12), fg="white", bg="#2c2c2c")
        self.timer_label.pack(pady=10)

    def update_timer(self):
        minutes, seconds = self.remaining_time // 60, self.remaining_time % 60
        self.timer_label.config(text=f"Time: {minutes}:{seconds:02}")
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.update_buttons(reveal_all_bombs=True)
            self.show_game_over(won=False)

    def setup_game_board(self):
        self.initialize_game_logic()
        self.create_board_frame()
        self.create_board_buttons()

    def initialize_game_logic(self):
        self.game = MinesweeperLogic(self.rows, self.cols, self.bombs)

    def create_board_frame(self):
        self.board_frame = tk.Frame(self.root, bg="#2c2c2c", padx=10, pady=10)
        self.board_frame.pack()

    def create_board_buttons(self):
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                self.create_button(row, col)

    def create_button(self, row, col):
        button = tk.Button(
            self.board_frame,
            text="",
            width=3,
            height=1,
            bg="#4d4d4d",  # medium dark gray
            relief="raised",
            font=("Arial", 12, "bold"),
            command=lambda: self.reveal_cell(row, col),
        )
        button.bind("<Button-3>", lambda event: self.place_flag(row, col))
        button.grid(row=row, column=col, padx=1, pady=1)
        self.buttons[row][col] = button

    def update_buttons(self, reveal_all_bombs=False):
        for row in range(self.rows):
            for col in range(self.cols):
                self.update_button(row, col, reveal_all_bombs)

    def update_button(self, row, col, reveal_all_bombs):
        button = self.buttons[row][col]
        if self.game.revealed[row][col]:
            self.set_revealed_button(button, row, col)
        elif self.game.flags[row][col]:
            button.config(text="🚩", fg="red", bg="#4d4d4d", state="normal", relief="raised", disabledforeground="red")
        else:
            button.config(text="", bg="#4d4d4d", state="normal", relief="raised")

        if reveal_all_bombs and (row, col) in self.game.bombs and not self.game.revealed[row][col]:
            button.config(text="💣", bg="white", fg="violet", state="disabled", relief="sunken",
                          disabledforeground="violet")

    def set_revealed_button(self, button, row, col):
        if (row, col) in self.game.bombs:
            button.config(text="💣", bg="white", fg="violet", state="disabled", relief="sunken",
                          disabledforeground="violet")
        else:
            num = self.game.board[row][col]
            button.config(
                text=str(num) if num > 0 else "",
                fg="black",
                bg="white",
                state="disabled",
                relief="sunken",
            )

    def reveal_cell(self, row, col):
        result = self.game.reveal(row, col)

        if result == "BOOM! You hit a bomb. Game Over.":
            self.update_buttons(reveal_all_bombs=True)
            self.show_game_over(False)
        else:
            self.update_buttons()

            if self.game.is_won():
                self.show_game_over(True)

    def place_flag(self, row, col):
        self.game.place_flag(row, col)
        self.update_buttons()

    def show_game_over(self, won):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.update_buttons(reveal_all_bombs=not won)

        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].config(state="disabled")

        message = "Congratulations! You won!" if won else "Game Over. You lost."
        messagebox.showinfo("Game Over", message)
