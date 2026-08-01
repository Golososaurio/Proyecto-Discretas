import numpy as np
from collections import deque

class MapaInundacion:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        # 0 = cuadro libre, 1 = obstaculo
        self.grid = np.zeros((filas, columnas), dtype=int)
        self.distancias = None
        self.ordenVisita = []  # orden en que la ola tocó cada cuadro
        self.camino = []

    #Métodos para la construcción del mapa

    def crearObstaculo(self, fila, columna):
        '''Solo queda un cuadro como obstaculo en la posición de fila, columna elegida'''
        self.grid[fila, columna] = 1

    def crearObstaculoGrande(self, filaInicial, columnaInicial, filaFinal, columnaFinal):
        '''Se crea un cuadrado desde la posición inicial a la final'''
        self.grid[filaInicial:filaFinal + 1, columnaInicial:columnaFinal + 1] = 1

    def vecinos(self, pos):
        '''Método para validar si la ola puede avanzar por dicho cuadro'''
        fila, columna = pos
        candidatos = [(fila - 1, columna), (fila + 1, columna), (fila, columna - 1), (fila, columna + 1)]
        for nuevaFila, nuevaColumna in candidatos:
            if 0 <= nuevaFila < self.filas and 0 <= nuevaColumna < self.columnas:
                if self.grid[nuevaFila, nuevaColumna] == 0:
                    yield(nuevaFila, nuevaColumna)

    #Algoritmo de inundación

    def inundar(self, inicio, fin):
        """Ejecuta la inundacion desde inicio y devuelve el camino como una lista de tuplas (fila, columna), o None si no hay camino posible"""
        if self.grid[inicio] == 1 or self.grid[fin] == 1:
            raise ValueError("El inicio o el fin están sobre un obstaculo")

        self.distancias = np.full((self.filas, self.columnas), -1, dtype=int)
        self.ordenVisita = []

        cola = deque([inicio])
        self.distancias[inicio] = 0

        while cola:
            actual = cola.popleft()
            self.ordenVisita.append(actual)

            if actual == fin:
                break

            for vecino in self.vecinos(actual):
                if self.distancias[vecino] == -1:
                    self.distancias[vecino] = self.distancias[actual] + 1
                    cola.append(vecino)

        if self.distancias[fin] == -1:
            self.camino = []
            return None

        #Se reconstruye el camino para saber cuál es el camino más corto
        camino = [fin]
        actual = fin
        while actual != inicio:
            fila, columna = actual
            for nuevaFila, nuevaColumna in [(fila - 1, columna), (fila + 1, columna), (fila, columna - 1), (fila, columna + 1)]:
                if 0 <= nuevaFila < self.filas and 0 <= nuevaColumna < self.columnas:
                    if self.distancias[nuevaFila, nuevaColumna] == self.distancias[actual] - 1:
                        actual = (nuevaFila, nuevaColumna)
                        camino.append(actual)
                        break
        camino.reverse()
        self.camino = camino
        return camino