import random
from Utils import *
class AVLNode:
    def __init__(self, board, value, left=None, right=None):
        self.board = board
        self.value = value
        self.left = left
        self.right = right
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None  # El árbol comienza vacío

    # Insertar un nuevo nodo en el árbol
    def insert(self, board, value):
        if not board:
            print("Intentando insertar un tablero inválido (None)")
            return
        self.root = self._insert(self.root, board, value)

    def _insert(self, node, board, value):
        if not node:
            return AVLNode(board, value)

        if value < node.value:
            node.left = self._insert(node.left, board, value)
        else:
            node.right = self._insert(node.right, board, value)

        # Actualizar la altura del nodo
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Balancear el árbol
        balance = self._get_balance(node)

        # Rotaciones según el balance
        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)

        if balance < -1 and value > node.right.value:
            return self._rotate_left(node)

        if balance > 1 and value > node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node
    
    # Método para obtener la altura de un nodo
    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    # Método para obtener el balance de un nodo
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    # Rotación a la derecha
    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        # Realizar la rotación
        x.right = y
        y.left = T2

        # Actualizar las alturas
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    # Rotación a la izquierda
    def _rotate_left(self, x):
        y = x.right
        T2 = y.left

        # Realizar la rotación
        y.left = x
        x.right = T2

        # Actualizar las alturas
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    # Obtener el mejor movimiento basado en la heurística
    def get_best_move(self, board):
    # Dimensiones del tablero
        ROWS = len(board)
        COLS = len(board[0])
    
        # 1. Verificar si la IA puede ganar en el próximo movimiento
        for col in range(COLS):
            if not self.is_column_full(board, col):
                temp_board = deepcopy(board)
                drop_piece(temp_board, col, 2)  # La IA es el jugador 2
                if check_winner(temp_board) == 2:    # Verificar si la IA gana con este movimiento
                    return col

        # 2. Verificar si el jugador podría ganar en el próximo movimiento y bloquear
        for col in range(COLS):
            if not self.is_column_full(board, col):
                temp_board = deepcopy(board)
                drop_piece(temp_board, col, 1)  # El jugador es el jugador 1
            if check_winner(temp_board) == 1:    # Verificar si el jugador gana con este movimiento
                return col

    # 3. Elegir una estrategia adicional si no hay una jugada inmediata de ganar o bloquear
    # En este caso, elige una columna aleatoria que no esté llena
        for col in range(COLS):
            if not self.is_column_full(board, col):
                return col

        print("No hay columnas disponibles, eligiendo un movimiento aleatorio.")
        # Si no se encuentra un mejor movimiento, elegir uno aleatorio
        return random.choice([col for col in range(7) if not self.is_column_full(board, col)])

    def is_column_full(self, board, col):
        return board[0][col] != 0  # Si la primera fila tiene un valor distinto de 0, la columna está llena

    def simulate_move(self, board, column, player):
        for row in range(5, -1, -1):
            if board[row][column] == 0:
                board[row][column] = player
                break

    def _get_best_move(self, node, board):
        if node is None:
            print("El Árbol está vacío, no se puede encontrar movimiento")
            return None

        best_value = float('-inf')
        best_board = None

        stack = [node]
        while stack:
            current_node = stack.pop()
            if current_node:
                current_value = self.evaluate_board(current_node.board, board)
                print(f"Evaluando tablero con valor heurístico: {current_value}")

            if current_value > best_value:
                best_value = current_value
                best_board = current_node.board
                print(f"Nuevo mejor tablero encontrado con valor: {best_value}")

            if current_node.left:
                stack.append(current_node.left)
            if current_node.right:
                stack.append(current_node.right)

        if best_board is None:
            raise ValueError("No se encontró ningún tablero adecuado")
        
        return  best_board

    # Método que compara el tablero actual con otros tableros para determinar la diferencia (movimiento)
    def extract_move_from_board(self, original_board, best_board):
    # Recorrer ambas matrices y comparar para encontrar la columna donde ocurrió la jugada
        for col in range(7):
            for row in range(6):
                if original_board[row][col] != best_board[row][col]:
                    return col  # Retornar la columna en la que se hizo el movimiento
    
    # Si no encuentra ninguna diferencia (lo cual es raro, pero posible), retornar un valor por defecto
        return -1  # O cualquier valor que maneje tu código para indicar que no hubo un cambio


    # Función para evaluar el tablero y asignar un valor heurístico
    def evaluate_board(self, board, current_board):
        value = 0
        
        # Aquí puedes agregar lógica personalizada para evaluar el estado del tablero
        # Se puede analizar cuántas alineaciones de 4 fichas están cerca de completarse
        # También se puede penalizar o premiar por bloquear o permitir jugadas del oponente

        for row in range(6):
            for col in range(7):
                if board[row][col] == 2:  # Ficha de la máquina (jugador 2)
                    value += self.evaluate_position(board, row, col, 2)
                elif board[row][col] == 1:  # Ficha del jugador humano (jugador 1)
                    value -= self.evaluate_position(board, row, col, 1)
        
        return value

    # Evaluar una posición dada
    def evaluate_position(self, board, row, col, player):
        # Verificar en las 4 direcciones posibles (horizontal, vertical, y ambas diagonales)
        score = 0
        score += self.evaluate_line(board, row, col, 0, 1, player)  # Horizontal
        score += self.evaluate_line(board, row, col, 1, 0, player)  # Vertical
        score += self.evaluate_line(board, row, col, 1, 1, player)  # Diagonal \
        score += self.evaluate_line(board, row, col, 1, -1, player) # Diagonal /

        return score

    # Evaluar una línea desde una posición dada en una dirección
    def evaluate_line(self, board, row, col, delta_row, delta_col, player):
        score = 0
        count = 0

        # Recorrer en ambas direcciones a partir de la posición dada
        for i in range(-3, 4):  # Chequea 3 posiciones antes y después
            r = row + i * delta_row
            c = col + i * delta_col

            if 0 <= r < 6 and 0 <= c < 7:
                if board[r][c] == player:
                    count += 1
                else:
                    count = 0  # Si se interrumpe la secuencia, reiniciar el conteo

                if count == 4:
                    score += 1000  # Cuatro en línea
                elif count == 3:
                    score += 10  # Tres en línea
                elif count == 2:
                    score += 1  # Dos en línea

        return score

def print_detailed_tree(self):
    self._print_detailed_tree(self.root)

def _print_detailed_tree(self, node, level=0, side="root"):
    if node is not None:
        indent = "   " * level
        print(f"{indent}- {side} -> Valor: {node.value}, Altura: {node.height}, Tablero: {node.board}")
        self._print_detailed_tree(node.left, level + 1, "izquierda")
        self._print_detailed_tree(node.right, level + 1, "derecha")