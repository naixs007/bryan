import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import heapq
from models.graph import Grafo
class Utils:
    @staticmethod
    def bfs(grafo, inicio, evitar=None):
        if evitar is None:
            evitar = []

        visitados = set()
        cola = [(inicio, [])]  # (Nodo actual, ruta hasta aquí)

        while cola:
            actual, ruta = cola.pop(0)

            if actual in visitados or actual in evitar:
                continue

            visitados.add(actual)

            # Si encontramos un nodo válido, retornamos la ruta
            for vecino in grafo.get_neighbors(actual):
             if vecino not in visitados and vecino not in evitar:
                    nueva_ruta = ruta + [vecino]
                    cola.append((vecino, nueva_ruta))
                    return nueva_ruta  # Tomamos el primer paso hacia el nodo

        return []  # No se encontró ruta









    @staticmethod
    def dijkstra(grafo, inicio, destino=None):
        distancias = {nodo: float('inf') for nodo in grafo.obtener_estado_grafo()}
        distancias[inicio] = 0
        cola = [(0, inicio)]  # (distancia, nodo)
        caminos = {inicio: []}

        while cola:
            distancia_actual, nodo = heapq.heappop(cola)
        
            if nodo == destino:  # Termina si se alcanza el destino
                return caminos[nodo]

            for vecino in grafo.obtener_estado_grafo().get(nodo, []):
                nueva_distancia = distancia_actual + grafo.get_distance(nodo, vecino)
            
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                heapq.heappush(cola, (nueva_distancia, vecino))
                caminos[vecino] = caminos[nodo] + [vecino]

        # Si destino es None, devuelve todos los caminos
        return caminos if destino is None else []
