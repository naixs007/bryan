from copy import deepcopy

def drop_piece(board, column, player):
    for row in range(5, -1, -1):
        if board[row][column] == 0:
            board[row][column] = player
            return True
    return False

def check_winner(board):
    ROWS = len(board)
    COLS = len(board[0])

    # Comprobar filas (horizontal)
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] and board[row][col] != 0:
                return board[row][col]

    # Comprobar columnas (vertical)
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] and board[row][col] != 0:
                return board[row][col]

    # Comprobar diagonales (de izquierda a derecha)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] and board[row][col] != 0:
                return board[row][col]

    # Comprobar diagonales (de derecha a izquierda)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if board[row][col] == board[row + 1][col - 1] == board[row + 2][col - 2] == board[row + 3][col - 3] and board[row][col] != 0:
                return board[row][col]

    return None