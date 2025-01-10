from gamelogic.minesweeper_logic import MinesweeperLogic

if __name__ == "__main__":
    rows, cols, num_bombs = 5, 5, 5
    game = MinesweeperLogic(rows, cols, num_bombs)
    game.display_board()

    while not game.game_over:
        print()
        print("Enter your move reveal/flag (row, col): ")
        move = input().split()
        row, col = int(move[1]), int(move[2])
        if move[0] == "reveal":
            result = game.reveal(row, col)
        elif move[0] == "flag":
            result = game.place_flag(row, col)
        else:
            result = "Invalid move!"
        game.display_board()
