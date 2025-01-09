import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.character import Personaje

class Policia(Personaje):
    def __init__(self, nombre, posicion):
        super().__init__(nombre, posicion)

