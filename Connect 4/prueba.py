import random

def create_board():
    return [[0 for _ in range(7)] for _ in range(6)]

def print_board(board):
    for row in board:
        print(' | '.join(str(cell) if cell != 0 else '.' for cell in row))
    print('-' * 29)

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

def drop_piece(board, col, piece):
    for row in range(5, -1, -1):  # Comenzar desde la última fila
        if board[row][col] == 0:
            board[row][col] = piece
            return True
    return False

def winning_move(board, piece):
    # Verifica si el movimiento de una pieza lleva a la victoria
    for col in range(7):
        # Simular el movimiento
        for row in range(5, -1, -1):
            if board[row][col] == 0:  # Si la celda está vacía
                board[row][col] = piece
                if check_winner(board) == piece:
                    board[row][col] = 0  # Revertir el movimiento
                    return col
                board[row][col] = 0  # Revertir el movimiento
                break
    return None

def ai_move(board):
    # Primero, la IA intenta ganar
    move = winning_move(board, 2)
    if move is not None:
        return move

    # Luego, la IA intenta bloquear al jugador
    move = winning_move(board, 1)
    if move is not None:
        return move

    # Si no hay victoria o bloqueo, elegir aleatoriamente
    while True:
        col = random.randint(0, 6)  # Columna aleatoria entre 0 y 6
        if board[0][col] == 0 :  # Colocamos ficha de la IA (2)
            return col

def main():
    board = create_board()
    game_over = False
    turn = 0

    while not game_over:
        print_board(board)

        if turn % 2 == 0:
            # Turno del jugador humano
            col = int(input("Jugador (Rojo), elige una columna (0-6): "))
            piece = 1  # Ficha roja
            
            if drop_piece(board, col, piece):
                winner = check_winner(board)
                if winner:
                    print_board(board)
                    print(f"¡Jugador {winner} gana!")
                    game_over = True
                else:
                    turn += 1  # Solo cambiar de turno si el jugador tiene éxito
            else:
                print("Columna llena, elige otra columna.")
        else:
            # Turno de la IA
            print("Turno de la Máquina (Amarillo)...")
            col = ai_move(board)
            piece = 2  # Ficha amarilla
            
            drop_piece(board, col, piece)  # La IA coloca su ficha
            winner = check_winner(board)
            if winner:
                print_board(board)
                print(f"¡Jugador {winner} gana!")
                game_over = True
            else:
                turn += 1  # Solo cambiar de turno si la IA tiene éxito

if __name__ == "__main__":
    main()

