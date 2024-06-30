import sys
from dataclasses import dataclass
from typing import TextIO, Iterator, Optional

from algoritmia import VERSION
from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solutions

#  -------- COMPROBACIÓN DE LA VERSIÓN DE LA BIBLIOTECA algoritmia --------

# Necesitamos la versión 3.0.1 o superior
if list(map(int, VERSION.split('.'))) < [3, 0, 1]:
    print("ERROR: Necesitas una versión actualizada de la biblioteca 'algoritmia'.")
    print("CÓMO ACTUALIZAR: Se explicó cómo hacerlo en un mensaje al foro de la asignatura, "
          "que recibiste como notificación en tu correo, el 15 de noviembre.")
    exit(1)

# ---------------------------------------- Tipos ----------------------------------------

# Un azulejo es una cadena de 0s y 1s de longitud 4 (p. ej. '0101'):
#  - La posición en la cadena indica uno de los 4 lados del azulejo: left, up, right, down.
#  - El caracter ('0 o '1') represent el color.
Tile = str

# Una solución es un tablero de azulejos, implementando como una lista de listas.
# Utiliza None para representar las casillas sin azulejo.
Board = list[list[Optional[Tile]]]
Solution = Board

# ---------------------------------------- Constantes ----------------------------------------

# Por comodidad, para evitar tener que usar directamente los enteros para left, up, right y down.
# Por ejemplo, si tile='1010', tile[R] es '1', el color de la zona derecha
L, U, R, D = 0, 1, 2, 3

# ---------------------------------------- IMPLEMENTAR ----------------------------------------
Decision = Tile
lista1: list[str] = ["1010", "0101", "1100", "0110", "0011", "1001"]


def process(num_rows: int, num_cols: int, tiles: list[Tile]) -> Iterator[Solution]:
    @dataclass
    class Extra:
        solucion: Board
        dicc: {}

    class TilesDS(DecisionSequence[Decision, Extra]):
        def solution(self) -> Solution:
            return self.extra.solucion

        def is_solution(self) -> bool:
            return len(self.extra.solucion) == num_rows and len(self.extra.solucion[-1]) == num_cols

        def successors(self) -> Iterator[Board]:
            n = len(self)
            if n < (num_rows * num_cols)-1:  # Si quedan decisiones por tomar
                if n < num_cols-1:  # primera fila [0]
                    tile1 = self.extra.solucion[0][n]
                    if n < num_cols - 2:
                        for til in self.extra.dicc:
                            if self.extra.dicc[til] > 0 and til[L] == tile1[R]:
                                self.extra.solucion[0].append(til)
                                self.extra.dicc[til] -= 1
                                yield self.add_decision(til, Extra(self.extra.solucion, self.extra.dicc))
                                self.extra.solucion[0].pop()
                                self.extra.dicc[til] += 1
                    else:  # ultimo
                        tile2 = self.extra.solucion[0][0]
                        for til in self.extra.dicc:
                            if self.extra.dicc[til] > 0 and tile1[R] == til[L] and til[R] == tile2[L]:
                                self.extra.solucion[0].append(til)
                                self.extra.dicc[til] -= 1
                                yield self.add_decision(til, Extra(self.extra.solucion, self.extra.dicc))
                                self.extra.solucion[0].pop()
                                self.extra.dicc[til] += 1
                elif num_cols - 2 < n < (num_cols * (num_rows - 1))-1:  # entre primera fila y la ultima
                    fila = (n + 1) // num_cols
                    columna = (n + 1) % num_cols
                    if columna == 0:  # primero, arriba
                        tile3 = self.extra.solucion[fila - 1][0]  # arriba
                        for til in self.extra.dicc:
                            if self.extra.dicc[til] > 0 and til[U] == tile3[D]:
                                self.extra.solucion.append([til])
                                self.extra.dicc[til] -= 1
                                yield self.add_decision(til, Extra(self.extra.solucion, self.extra.dicc))
                                self.extra.solucion.pop()
                                self.extra.dicc[til] += 1
                    elif columna == num_cols - 1:  # ultimo
                        tile1 = self.extra.solucion[-1][columna - 1]  # iz
                        tile4 = self.extra.solucion[-1][0]  # de
                        tile3 = self.extra.solucion[fila - 1][columna]  # arriba
                        for til in self.extra.dicc:
                            if self.extra.dicc[til] > 0 and til[U] == tile3[D] and til[L] == tile1[R] and til[R] == tile4[L]:
                                self.extra.solucion[-1].append(til)
                                self.extra.dicc[til] -= 1
                                yield self.add_decision(til, Extra(self.extra.solucion, self.extra.dicc))
                                self.extra.solucion[-1].pop(-1)
                                self.extra.dicc[til] += 1
                    else:  # medio
                        tile1 = self.extra.solucion[-1][columna - 1]  # iz
                        tile3 = self.extra.solucion[fila - 1][columna]  # arriba
                        for til in self.extra.dicc:
                            if self.extra.dicc[til] > 0 and til[U] == tile3[D] and til[L] == tile1[R]:
                                self.extra.solucion[-1].append(til)
                                self.extra.dicc[til] -= 1
                                yield self.add_decision(til, Extra(self.extra.solucion, self.extra.dicc))
                                self.extra.solucion[-1].pop(-1)
                                self.extra.dicc[til] += 1
                else:  # ultima fila
                    fila = (n+1)//num_cols
                    columna = (n + 1) % num_cols
                    if columna == 0:  # primero, arriba abajo
                        tile2 = self.extra.solucion[0][0]  # "abajo"
                        tile3 = self.extra.solucion[fila-1][0]  # arriba
                        for til in self.extra.dicc:
                            if self.extra.dicc[til] > 0 and tile2[U] == til[D] and til[U] == tile3[D]:
                                self.extra.solucion.append([til])
                                self.extra.dicc[til] -= 1
                                yield self.add_decision(til, Extra(self.extra.solucion, self.extra.dicc))
                                self.extra.solucion.pop()
                                self.extra.dicc[til] += 1
                    elif columna == num_cols - 1:  # ultimo U , D , R , L
                        tile1 = self.extra.solucion[-1][columna-1]  # iz
                        tile4 = self.extra.solucion[-1][0]  # de
                        tile2 = self.extra.solucion[0][-1]  # "abajo"
                        tile3 = self.extra.solucion[fila - 1][columna]  # arriba
                        for til in self.extra.dicc:
                            if self.extra.dicc[til] > 0 and tile2[U] == til[D] and til[U] == tile3[D] and til[L] == tile1[R] and til[R] == tile4[L]:
                                self.extra.solucion[-1].append(til)
                                self.extra.dicc[til] -= 1
                                yield self.add_decision(til, Extra(self.extra.solucion, self.extra.dicc))
                                self.extra.solucion[-1].pop(-1)
                                self.extra.dicc[til] += 1
                    else:  # mitad U , D , L
                        tile1 = self.extra.solucion[-1][columna - 1]  # iz
                        tile2 = self.extra.solucion[0][columna]  # "abajo"
                        tile3 = self.extra.solucion[fila - 1][columna]  # arriba
                        for til in self.extra.dicc:
                            if self.extra.dicc[til] > 0 and tile2[U] == til[D] and til[U] == tile3[D] and til[L] == tile1[R]:
                                self.extra.solucion[-1].append(til)
                                self.extra.dicc[til] -= 1
                                yield self.add_decision(til, Extra(self.extra.solucion, self.extra.dicc))
                                self.extra.solucion[-1].pop(-1)
                                self.extra.dicc[til] += 1
    diccionario = {"1010": 0, "0101": 0, "1100": 0, "0110": 0, "0011": 0, "1001": 0}
    for indice in tiles[1:]:
        diccionario[indice] += 1
    sol: list[list[Optional[Tile]]] = [[tiles[0]]]
    initial_ds = TilesDS(Extra(sol, diccionario))
    return bt_solutions(initial_ds)
# -------------------------- No modificar el código a partir de esta línea ---------------------

def read_data(f: TextIO) -> tuple[int, int, list[Tile]]:  # (rows, cols, list_of_tiles):
    num_rows, num_cols = map(int, f.readline().split())
    tiles = [line.strip() for line in f]
    return num_rows, num_cols, tiles


def show_results(all_solutions: Iterator[Solution]):
    for i, sol in enumerate(all_solutions):
        print(f"# {i + 1}:")
        for row in sol:
            print(' '.join(f"{e:>2}" for e in row))

# ---------------------------------------- programa principal ----------------------------------------

if __name__ == "__main__":
    num_rows0, num_cols0, tiles0 = read_data(sys.stdin)
    all_solutions0 = process(num_rows0, num_cols0, tiles0)
    show_results(all_solutions0)
