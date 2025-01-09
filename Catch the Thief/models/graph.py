class Grafo:
    def __init__(self):
        self.nodos = {}  # Mantenemos los nodos del grafo
    
    def agregar_nodo(self, nodo):
        if nodo not in self.nodos:
            self.nodos[nodo] = [] 
        else:
            raise ValueError(f"El nodo {nodo} ya existe en el grafo.")
    
    def agregar_arista(self, nodo_origen, nodo_destino):
        if nodo_origen in self.nodos and nodo_destino in self.nodos:
            if nodo_destino not in self.nodos[nodo_origen]:
                self.nodos[nodo_origen].append(nodo_destino)
            if nodo_origen not in self.nodos[nodo_destino]:
                self.nodos[nodo_destino].append(nodo_origen)
        else:
            raise ValueError("Ambos nodos deben existir en el grafo.")
    
    def agregar_nodos_iniciales(self, nodos_iniciales, aristas_iniciales):
        """Método mejorado para agregar nodos y aristas iniciales """
        for nodo in nodos_iniciales:
            self.agregar_nodo(nodo)
        
        for nodo_origen, nodo_destino in aristas_iniciales:
            self.agregar_arista(nodo_origen, nodo_destino)
    
    def obtener_estado_grafo(self):
        """Devuelve el estado actual de los nodos y sus conexiones."""
        return self.nodos
    
    def actualizar_estado(self, policias, ladron):
        """Actualiza el estado del grafo con las posiciones de los policías y el ladrón."""
        estado = {nodo: list(conexiones) for nodo, conexiones in self.nodos.items()}
        
        # Aquí, estamos asumiendo que policias y ladron tienen el atributo `posicion`
        for policia in policias:
            estado[policia.posicion] = "P"  # "P" para policía
        estado[ladron.posicion] = "L"  # "L" para ladrón
        
        return estado
    
    def get_neighbors(self, nodo):
        """Devuelve los nodos adyacentes a un nodo dado."""
        return self.nodos.get(nodo, [])
    
    def get_distance(self, nodo1, nodo2):
        """
        Devuelve la distancia entre dos nodos. Asumimos que todas las aristas tienen distancia 1.
        Si el grafo es ponderado, este método debería ser ajustado para retornar el peso real.
        """
        if nodo2 in self.nodos[nodo1]:
            return 1  # Asumimos distancia 1 entre nodos adyacentes.
        return float('inf')  # Si no están conectados, devolvemos infinito.

