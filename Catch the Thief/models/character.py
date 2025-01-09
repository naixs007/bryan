class Personaje:
    def __init__(self, nombre, posicion):
        self.nombre = nombre
        self.posicion = posicion

    def mover(self, nueva_posicion):
        """
        Cambia la posición del personaje.
        """
        self.posicion = nueva_posicion
