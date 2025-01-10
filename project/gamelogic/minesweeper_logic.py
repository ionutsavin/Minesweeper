import random


def is_neighbor(row, col, exclude):
    """
    Check if the cell at (row, col) is a neighbor of the cell at exclude

    Args:
        row, col (int): the row and column of the cell to check
    Returns:
        bool: True if the cell at (row, col) is a neighbor of the cell at exclude, False otherwise
    """
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
        """
        Places bombs on the board, excluding the cell at exclude

        Args:
            exclude (tuple): the row and column of the cell to exclude from placing a bomb
        """
        while len(self.bombs) < self.num_bombs:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if ((row, col) != exclude and (row, col) not in self.bombs
                    and not is_neighbor(row, col, exclude)):
                self.bombs.add((row, col))

    def calculate_numbers(self):
        """ Calculate the number of bombs adjacent to each cell """
        for row, col in self.bombs:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    neighbour_row, neighbour_col = row + dr, col + dc
                    if (0 <= neighbour_row < self.rows and 0 <= neighbour_col < self.cols
                            and (neighbour_row, neighbour_col) not in self.bombs):
                        self.board[neighbour_row][neighbour_col] += 1

    def reveal(self, row, col):
        """
        Reveal the cell at (row, col)

        Args:
            row, col (int): the row and column of the cell to reveal
        Returns:
            str: the result of revealing the cell
        """
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

    def print_bombs(self):
        """ Print the board with bombs """
        for row in range(self.rows):
            for col in range(self.cols):
                print("B" if (row, col) in self.bombs else "-", end=" ")
            print()

    def place_flag(self, row, col):
        """
        Place or remove a flag on the cell at (row, col)

        Args:
            row, col (int): the row and column of the cell to place a flag
        Returns:
            str: the result of placing a flag
        """
        if not self.is_valid_coordinate(row, col):
            return "Invalid coordinates!"

        if self.revealed[row][col]:
            return f"Cell ({row}, {col}) is already revealed! Cannot place a flag."

        self.flags[row][col] = not self.flags[row][col]

    def is_valid_coordinate(self, row, col):
        """
        Check if the coordinate (row, col) is valid

        Args:
            row, col (int): the row and column to check
        Returns:
            bool: True if the coordinate is valid, False otherwise
        """
        return 0 <= row < self.rows and 0 <= col < self.cols

    def reveal_all_bombs(self):
        """ Reveal all bombs on the board """
        for row, col in self.bombs:
            self.revealed[row][col] = True
        return "BOOM! You hit a bomb. Game Over."

    def reveal_cell(self, row, col):
        """
        Reveal the cell at (row, col) and recursively reveal its neighbors

        Args:
            row, col (int): the row and column of the cell to reveal
        """
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
        """ Check if the game is won """
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.revealed[row][col] and (row, col) not in self.bombs:
                    return False
        return True
