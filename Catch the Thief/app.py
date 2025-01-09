from flask import Flask, render_template, jsonify, request
from controller.game_controller import GameController

app = Flask(__name__)

game = GameController()

@app.route('/')
def index():
    # Verifica si el juego ha sido inicializado, si no, inicialízalo
    if not game.ladron or not game.policias:  # Si el juego no tiene ladron o policias, inicializar
        game.inicializar_juego()
    
    estado = game.get_estado()
    return render_template('index.html', estado=estado)

@app.route('/mover_policia', methods=['POST'])
def mover_policia():
    data = request.json
    indice = data['indice']
    nueva_posicion = data['nueva_posicion']
    if game.mover_policia(indice, nueva_posicion):
        game.mover_ladron()  # Mueve al ladrón después de que el usuario mueve un policía
        print("Estado del tablero después de una interacción del usuario:")
        print(game.get_estado())
    return jsonify(game.get_estado())

@app.route('/actualizar_dificultad', methods=['POST'])
def actualizar_dificultad():
    try:
        data = request.json  # Obtener los datos enviados en formato JSON
        if not data:
            return jsonify({'mensaje': 'No se enviaron datos'}), 400
        
        dificultad = data.get('difficulty')  # Obtener el valor de 'difficulty'
        if dificultad not in ['easy', 'hard']:
            return jsonify({'mensaje': 'Dificultad inválida'}), 400
        
        # Actualizar el modo de dificultad del juego
        game.modo_dificultad = dificultad
        return jsonify({'mensaje': 'Dificultad actualizada correctamente', 'dificultad': dificultad})
    
    except Exception as e:
        # Capturar cualquier error y devolver información detallada
        print(f"Error: {e}")
        return jsonify({'mensaje': 'Ocurrió un error en el servidor', 'error': str(e)}), 500


@app.route('/mover_ladron', methods=['POST'])
def mover_ladron():
    data = request.json
    nueva_posicion = data['nueva_posicion']
    game.mover_ladron(nueva_posicion)
    return jsonify(game.get_estado())

@app.route('/reiniciar', methods=['POST'])
def reiniciar():
    global game
    game.inicializar_juego()  # Inicializa el juego
    estado_inicial = {
        'ladron': game.ladron.posicion,
        'policias': [policia.posicion for policia in game.policias]
    }
    return jsonify({"mensaje": "Juego reiniciado", "estado": estado_inicial})

if __name__ == '__main__':
    app.run(debug=True)


