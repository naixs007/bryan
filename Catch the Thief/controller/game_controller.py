import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.graph import Grafo
from models.police import Policia
from models.thief import Ladron
from controller.utils import Utils  # Para acceder a los algoritmos de movimiento
from flask import jsonify

class GameController:
    def __init__(self, modo_dificultad="dificil"):
        self.modo_dificultad = modo_dificultad  # "facil" o "dificil"
        self.inicializar_juego()
    
    def inicializar_juego(self):
        self.grafo = Grafo()
        self.grafo.agregar_nodos_iniciales(
        ["N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "N10"],
        [("N1", "N2"), ("N1", "N4"), ("N1", "N5"),
         ("N2", "N3"), ("N2", "N5"),
         ("N3", "N5"), ("N3", "N6"),
         ("N4", "N5"), ("N4", "N7"),
         ("N5", "N6"), ("N5", "N7"), ("N5", "N8"), ("N5", "N9"),
         ("N6", "N9"),
         ("N7", "N8"), ("N7", "N10"),
         ("N8", "N9"), ("N8", "N10"),
         ("N9", "N10")]
    )
        self.policias = [
            Policia("P1", "N1"),
            Policia("P2", "N2"),
            Policia("P3", "N3")
        ]
        self.ladron = Ladron("L", "N8")

    def mover_policia(self, indice, nueva_posicion):
        if nueva_posicion in self.grafo.get_neighbors(self.policias[indice].posicion):
            if not any(policia.posicion == nueva_posicion for policia in self.policias): 
                self.policias[indice].mover(nueva_posicion)
                self.mover_ladron()  # El ladrón se mueve después de que un policía se mueva
                return jsonify(self.get_estado()), 200  # Retornar el estado actualizado
            else:
                return jsonify({"mensaje": f"La posición {nueva_posicion} ya está ocupada por otro policía."}), 400
        else:
        
            return jsonify({"mensaje": f"La posición {nueva_posicion} no es válida."}), 400

    

    def actualizar_dificultad(self, dificultad):
        """Actualizar el modo de dificultad (facil o dificil)"""
        if dificultad in ["Fácil", "Difícil"]:
            self.modo_dificultad = dificultad
            return jsonify({"mensaje": f"Dificultad actualizada a {dificultad}"}), 200
        else:
            return jsonify({"mensaje": "Dificultad no válida."}), 400


    def mover_ladron(self):
        """El ladrón se mueve según el modo de dificultad: BFS para fácil, Dijkstra para difícil."""
        if self.modo_dificultad == "Fácil":
            # Mover con un algoritmo menos eficiente, como BFS
            ruta = Utils.bfs(self.grafo, self.ladron.posicion)
        elif self.modo_dificultad == "Difícil":
            # Mover con Dijkstra
            ruta = Utils.dijkstra(self.grafo, self.ladron.posicion)
        
        # El ladrón se mueve al primer nodo en la ruta
        if ruta:
            print(f"Ruta calculada para el ladrón: {ruta}")
            self.ladron.mover(ruta[0])  # Tomamos el siguiente paso en la ruta calculada
            print(f"Ladrón movido a {self.ladron.posicion}")
        else:
            print("No hay movimiento posible para el ladrón.")

    def get_estado(self):
        estado = self.grafo.actualizar_estado(self.policias, self.ladron)
        return estado
    
    def reiniciar(self):
        self.inicializar_juego()

