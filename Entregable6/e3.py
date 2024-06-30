import random
import sys
from collections.abc import Iterator
from random import seed
from time import process_time
from typing import TextIO

from algoritmia.datastructures.graphs import UndirectedGraph, WeightingFunction
from algoritmia.utils import infinity

# ---------- CONSTANTE  ----------

TIMEOUT = 2.0  # Segundos disponibles para el process

# ---------- TIPOS ----------

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]

# Un problema se define como una tupla de tres elementos:
#  - un grafo no dirigido y conexo, g.
#  - una función, wf, con los pesos de las aristas de dicho grafo. Peso de la arista (u,v): wf(u,v)
#  - un conjunto de vertices a visitar, vertices_to_visit.
# Problem = (g, wf, vertices_to_visit)
Problem = tuple[UndirectedGraph[Vertex], WeightingFunction[Vertex], set[Vertex]]

# Queremos encontrar un camino cerrado que pase por vertices_to_visit y tenga la menor longitud posible.
# Una solución es una tupla de dos elementos:
# - Un flotante, length, con la longitud del camino (la suma de las distancias de las aristas utilizadas en el camino).
# - Una lista de vertices, path, que representa el camino, el primer y el último vértice deben ser el mismo.
# Solution = (length, path)
Solution = tuple[float, list[Vertex]]


# ---------- IMPLEMENTAR ESTA FUNCIÓN COMO UN GENERADOR DE SOLUCIONES ----------

def greedy_solutions(problem: Problem) -> Iterator[Solution]:
    # g es un grafo no dirigido y conexo, cuyos vértices son tuplas de dos enteros
    # Dada una arista (u, v) de g, puedes obtener su peso con wf(u, v)
    # vertices_to_visit es el conjunto de vértices a visitar en el camino cerrado
    g, wf, vertices_to_visit = problem
    # Esta función es un generador, puedes generar todas las soluciones que quieras.
    # Mira la definición del tipo Solution que está al principio de este fichero.

    while True:
        aux = vertices_to_visit
        peso = 0.0
        vertice_inicio = random.choice(list(aux))
        visitados: list[Vertex] = []
        visito = vertice_inicio
        visitados.append(vertice_inicio)
        while len(aux) > 0 or visito != vertice_inicio:
            vecinos = list(g.succs(visito))
            indices = list(range(len(vecinos)))
            sorted_indices = sorted(indices, key=lambda i: -wf(visito, vecinos[i]))
            vecino_cercano = vecinos[sorted_indices[0]]
            if visitados.count(vecino_cercano) >= 2:
                vecino_cercano = random.choice(list(vecinos))
            if vecino_cercano in aux:
                aux.remove(vecino_cercano)
            visitados.append(vecino_cercano)
            peso += wf(visito, vecino_cercano)
            visito = vecino_cercano
        yield peso, visitados


# ---------- NO MODIFICAR EL CÓDIGO A PARTIR DE ESTA LÍNEA ----------


# Distancia euclídea entre los dos vértices de una arista
def eu_distance(e: Edge) -> float:
    (ux, uy), (vx, vy) = e
    dx, dy = ux - vx, uy - vy
    return (dx * dx + dy * dy) ** 0.5


def read_data(f: TextIO) -> Problem:
    num_edges, num_vertices_to_visit = map(int, f.readline().split())
    es = []
    for _ in range(num_edges):
        ux, uy, vx, vy = map(int, f.readline().split())
        es.append(((ux, uy), (vx, vy)))
    wf = WeightingFunction(((e, eu_distance(e)) for e in es), symmetrical=True)
    vertices_to_visit = set()
    for _ in range(num_vertices_to_visit):
        x, y = map(int, f.readline().split())
        vertices_to_visit.add((x, y))
    return UndirectedGraph(E=es), wf, vertices_to_visit


def process(problem: Problem) -> Solution:
    seed(42)  # Fija la semilla para que el programa sea determinista
    best_length = infinity
    best_path = []
    t_start = process_time()
    for solution in greedy_solutions(problem):
        if process_time() - t_start > TIMEOUT:
            break
        assert check_solution(problem, solution) == "OK", check_solution(problem, solution)
        length, path = solution
        if length < best_length:
            best_length = length
            best_path = path[:]
    return best_length, best_path


def show_results(solution: Solution):
    length, path = solution
    print(f"{length:.2f}")
    for v in path:
        print(f"{v[0]} {v[1]}")


# ---------------------------------------- Comprobador de soluciones ----------------------------------------


# Dado un problema y su solución, comprueba que la solución sea válida
def check_solution(problem: Problem, solution: Solution) -> str:
    pre = "SOLUTION ERROR:"

    error_tipo_solution = f"{pre} La solución no tiene el formato correcto."
    if not isinstance(solution, tuple) or len(solution) != 2:
        return error_tipo_solution
    sol_length, sol_path = solution

    if (not isinstance(sol_length, float) or not isinstance(sol_path, list) or len(sol_path) == 0 or
            not isinstance(sol_path[0], tuple) or len(sol_path[0]) != 2 or not isinstance(sol_path[0][0], int)):
        return error_tipo_solution

    g, wf, vertices_to_visit = problem

    u = sol_path[0]
    calc_length = 0
    for v in sol_path[1:]:
        if (u, v) not in g.E and (v, u) not in g.E:
            return f"{pre} La arista {(u, v)} no pertenece al grafo."
        calc_length += wf(u, v)
        u = v
    if sol_path[0] not in vertices_to_visit:
        return f"{pre} El primer vértice debe pertenecer al conjunto vertices_to_visit."
    if sol_path[0] != sol_path[-1]:
        return f"{pre} El primer y el último vértice del ciclo deben ser el mismo."
    for v in vertices_to_visit:
        if v not in sol_path:
            return f"{pre} El ciclo no contine el vértice {v}, que pertenece al conjunto vertices_to_visit."
    if abs(calc_length - sol_length) > 0.1:
        return f"{pre} La longitud indicada ({sol_length:.2f}), no es correcta, debería ser {calc_length:.2f}."
    return "OK"


# ---------------------------------------- Program principal ----------------------------------------

if __name__ == "__main__":
    problem0 = read_data(sys.stdin)
    solution0 = process(problem0)
    show_results(solution0)
