import sys

from algoritmia.datastructures.queues import Fifo

if sys.version_info.major != 3 or sys.version_info.minor < 10:
    raise RuntimeError("This program needs Python3, version 3.10 or higher")

from typing import TextIO

from algoritmia.datastructures.graphs import UndirectedGraph

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]


def read_data(f: TextIO) -> tuple[
    UndirectedGraph[Vertex], int, int]:  # PODRIA PONER TAMBIEN LAS ARISTAS AL CONTRARIO PARA DOBLE SENTIDO??
    numfilas, numcolumnas = map(int, f.readline().split())
    corridors: list[Edge] = []
    for fil in range(numfilas):
        linea = f.readline().strip()
        numeros = [int(char) for char in linea]
        for col in range(numcolumnas):  # creacion del laberinto
            if numeros[col] == 1:
                corridors.append(((fil, col), (fil, col + 1)))

            elif numeros[col] == 2:
                corridors.append(((fil, col), (fil + 1, col)))

            elif numeros[col] == 3:
                corridors.append(((fil, col), (fil, col + 1)))
                corridors.append(((fil, col), (fil + 1, col)))
    return UndirectedGraph(E=corridors), numfilas, numcolumnas


def process(ug: UndirectedGraph[Vertex], rows: int, cols: int) -> int:
    # TODO: IMPLEMENTAR
    entrada: Vertex = 0, 0
    recorrido = rrecorrido(ug, entrada)

    return recorrido


def bf_search(g: UndirectedGraph[Vertex], source: Vertex, target: Vertex) -> list[Edge]:
    # Recorredor parecifo a traverser_bf (Transpa 15 Tema 2) (tiene que parar al llegar a target)
    queue: Fifo[Edge] = Fifo()  # Cola de aristas
    seen: set[Vertex] = set()  # Conjunto de vértices vistos
    queue.push((source, source))  # Añadimos la arista fantasma inicial
    seen.add(source)  # añadimos que visitamos el principio del laberinto
    res = []
    while len(queue) > 0:  # mientras tenga Edges que mirar del laberinto
        u, v = queue.pop()
        res.append((u, v))  # Añadimos una arista
        if v == target:  # si encontramos la salida paramos de buscar
            break
        for suc in g.succs(v):  # miro los vecinos del vertice
            if suc not in seen:
                queue.push((v, suc))  # lo añado a la cola para mirar sus vecinos si no esta visitado antes
                seen.add(suc)  # la lista donde pongo los vert vistos
    return res
def path_recover(edges: list[Edge], target: Vertex) -> list[Vertex]:
    # esta en la tranpa 39 del tema 2; crear diccionario bp a partir de edges; REcuperar el camino desde target hasta la arista fantasma; invertir el camino
    bp: dict[Vertex,Vertex]={}
    for u,v in edges:
        bp[v]=u
    t = target
    path = [t]
    while t != bp[t]:
        t=bp[t]
        path.append(t)
    path.reverse()
    return path

def rrecorrido(g: UndirectedGraph[Vertex], entrada: Vertex) -> int:
    queue: Fifo[Edge] = Fifo()  # Cola de aristas
    visitados: set[Vertex] = set()  # Conjunto de vértices vistos
    costes: dict[Vertex, int] = dict()
    coste = 1
    costes[entrada] = coste
    queue.push((entrada, entrada))
    visitados.add(entrada)
    direcciones = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # arriba,iz,der,abajo
    while len(queue) > 0:
        u, v = queue.pop()
        for dx, dy in direcciones:
            suc = (v[0] + dx, v[1] + dy)
            if suc in g.succs(v) and suc not in visitados:
                queue.push((v, suc))
                visitados.add(suc)
                coste += 1
                costes[suc] = coste
    lista = list(costes)
    suma = 0
    for v in range(coste - 1):
        a = bf_search(g, lista[v], lista[v + 1])
        path = path_recover(a,lista[v + 1])
        suma += len(path)-1

    return suma


def show_results(steps: int):
    print(steps)


if __name__ == "__main__":
    ug0, rows0, cols0 = read_data(sys.stdin)

    steps0 = process(ug0, rows0, cols0)
    show_results(steps0)
