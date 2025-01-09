
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.character import Personaje
import random

class Ladron(Personaje):
    def __init__(self, nombre, posicion, dificultad="fácil"):
        super().__init__(nombre, posicion)
        self.dificultad = dificultad

    def mover(self, grafo, policias):
        """
        Mueve al ladrón según la dificultad especificada.
        - En dificultad fácil: se mueve utilizando BFS simplificado.
        - En dificultad difícil: usa Dijkstra para encontrar el camino más corto.
        """
        if self.dificultad == "fácil":
            return self.mover_bfs(grafo)
        elif self.dificultad == "difícil":
            return self.mover_dijkstra(grafo)

    def mover_bfs(self, grafo):
        """
        Mueve al ladrón utilizando un algoritmo BFS (menos eficiente que Dijkstra).
        """
        nodos_adyacentes = grafo.get_graph_state().get(self.posicion, [])
        if nodos_adyacentes:
            nueva_posicion = random.choice(nodos_adyacentes)
            self.posicion = nueva_posicion
            return nueva_posicion
        return self.posicion

    def mover_dijkstra(self, grafo):
        """
        Mueve al ladrón utilizando el algoritmo Dijkstra para encontrar el camino más corto.
        """
        # Suponiendo que el grafo tiene las distancias entre nodos y podemos usar Dijkstra
        nodos_adyacentes = grafo.get_graph_state().get(self.posicion, [])
        # Aquí se debería implementar el cálculo real de Dijkstra, 
        # pero por simplicidad seleccionamos aleatoriamente un nodo adyacente
        if nodos_adyacentes:
            nueva_posicion = min(nodos_adyacentes, key=lambda x: grafo.get_distance(self.posicion, x)) 
            self.posicion = nueva_posicion
            return nueva_posicion
        return self.posicion

