import random


def is_neighbor(row, col, exclude):
    exclude_r, exclude_col = exclude
    return abs(row - exclude_r) <= 1 and abs(col - exclude_col) <= 1


class MinesweeperLogic:
    def __init__(self, rows, cols, num_bombs):
        self.rows = rows
        self.cols = cols
        self.num_bombs = num_bombs
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]
        self.bombs = set()
        self.game_over = False
        self.first_move = True

    def place_bombs(self, exclude):
        while len(self.bombs) < self.num_bombs:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if (row, col) != exclude and (row, col) not in self.bombs and not is_neighbor(row, col, exclude):
                self.bombs.add((row, col))

    def calculate_numbers(self):
        for row, col in self.bombs:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    neighbour_row, neighbour_col = row + dr, col + dc
                    if (0 <= neighbour_row < self.rows and 0 <= neighbour_col < self.cols
                            and (neighbour_row, neighbour_col) not in self.bombs):
                        self.board[neighbour_row][neighbour_col] += 1

    def reveal(self, row, col):
        if not self.is_valid_coordinate(row, col):
            return "Invalid coordinates!"

        if self.game_over:
            return "Game is already over!"

        if self.revealed[row][col]:
            return f"Cell ({row}, {col}) is already revealed!"

        if self.flags[row][col]:
            return f"Cell ({row}, {col}) is flagged! Remove the flag first to reveal."

        if self.first_move:
            self.first_move = False
            self.place_bombs((row, col))
            self.print_bombs()
            self.calculate_numbers()

        if (row, col) in self.bombs:
            self.game_over = True
            return self.reveal_all_bombs()

        self.reveal_cell(row, col)
        return None

    def print_bombs(self):
        for row in range(self.rows):
            for col in range(self.cols):
                print("B" if (row, col) in self.bombs else "-", end=" ")
            print()

    def place_flag(self, row, col):
        if not self.is_valid_coordinate(row, col):
            return "Invalid coordinates!"

        if self.revealed[row][col]:
            return f"Cell ({row}, {col}) is already revealed! Cannot place a flag."

        self.flags[row][col] = not self.flags[row][col]
        return None

    def is_valid_coordinate(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def reveal_all_bombs(self):
        for r, c in self.bombs:
            self.revealed[r][c] = True
        return "BOOM! You hit a bomb. Game Over."

    def reveal_cell(self, row, col):
        if not self.is_valid_coordinate(row, col) or self.revealed[row][col]:
            return

        self.revealed[row][col] = True

        if self.board[row][col] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    neighbour_row, neighbour_col = row + dr, col + dc
                    if (neighbour_row, neighbour_col) != (row, col):
                        self.reveal_cell(neighbour_row, neighbour_col)

    def is_won(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.revealed[r][c] and (r, c) not in self.bombs:
                    return False
        return True

    def board_state(self):
        state = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                if self.revealed[r][c]:
                    if (r, c) in self.bombs:
                        row.append("💣")
                    else:
                        num = self.board[r][c]
                        row.append(str(num) if num > 0 else "")
                elif self.flags[r][c]:
                    row.append("🚩")
                else:
                    row.append("")
            state.append(row)
        return state

    def display_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.revealed[r][c]:
                    if (r, c) in self.bombs:
                        print("💣", end=" ")
                    else:
                        num = self.board[r][c]
                        print(num if num > 0 else "", end=" ")
                elif self.flags[r][c]:
                    print("🚩", end=" ")
                else:
                    print("-", end=" ")
            print()
        print()
