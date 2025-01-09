from flask import Flask, render_template, jsonify, request
from avl_tree import AVLTree
from Utils import *

app = Flask(__name__)

# Crear el tablero inicial
board = [[0 for _ in range(7)] for _ in range(6)]
avl_tree = AVLTree()  # Árbol AVL para la IA
current_player = 1  # 1 = humano, 2 = máquina

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move/<int:column>', methods=['POST'])
def player_move(column):
    global current_player
    
    if drop_piece(board, column, current_player):
        if check_winner(board):
            return jsonify({"status": "win", "winner": current_player, "board": board})
        
        current_player = 2  # Cambio de turno a la máquina
    
    if current_player == 2:
        col = avl_tree.get_best_move(board)  # Obtener la mejor jugada de la máquina
        if col is not None and drop_piece(board, col, current_player):
            # Aquí se usa evaluate_board
            avl_tree.insert(deepcopy(board), avl_tree.evaluate_board(board, board))  # Insertar el estado en el árbol
            
            if check_winner(board):
                return jsonify({"status": "win", "winner": current_player, "board": board})  

        current_player = 1  # Volver al turno del jugador humano
              
    return jsonify({"status": "continue", "board": board, "current_player": current_player})


@app.route('/reset', methods=['POST'])
def reset_game():
    global board, current_player
    board = [[0 for _ in range(7)] for _ in range(6)]
    current_player = 1  # Comienza el jugador humano
    return jsonify({"status": "reset", "board": board})


if __name__ == '__main__':
    app.run(debug=True)
