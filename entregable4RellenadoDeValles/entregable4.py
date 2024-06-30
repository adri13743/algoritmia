from typing import TextIO
import sys


Solution = tuple[int, int, int]  # l, r, coste


def read_data(f: TextIO) -> list[int]:
    return [int(line) for line in f.readlines()]


def process(v: list[int]) -> Solution:
    def valle(l: int, r: int) -> Solution:
        if r - l < 2:      # No hay valle
            return 0, 1, 0

        if r - l == 2:
            centro = r - 1
            if r != len(v) and v[centro] < min(v[l], v[r]): # Si hay valle
                h = min(v[l], v[r])
                d = r - l - 1
                coste = d * h - v[centro]
                return l, r, coste
            else:
               return 0, 1, 0

        c = (l + r) // 2

        sol_izq = valle(l, c)
        sol_der = valle(c, r)

        in_der = r - 1
        in_izq = l
        sum_total = 0

        for i, j in zip(range(c + 1, r), range(c, l - 1, -1)):
            if v[i] >= min(v[in_izq], v[in_der]):
                if v[i] >= v[in_der]:
                    in_der = i
            elif v[j] >=  min(v[in_izq], v[in_der]):
                if v[j] >= v[in_izq]:
                    in_izq = j

        for k in range(in_izq + 1, in_der):
            if v[k] >= min(v[in_izq], v[in_der]):
                in_izq = k

        for k in range(in_izq + 1, in_der):
            sum_total += v[k]

        h = min(v[in_izq], v[in_der])
        d = in_der - in_izq - 1
        coste_centro = d * h - sum_total

        sol_centro: Solution = (in_izq, in_der, coste_centro)

        max_coste = max(sol_izq[2], sol_centro[2], sol_der[2])

        lista_sol: list[Solution] = [sol_izq, sol_centro, sol_der]

        for sol in lista_sol:
            if sol[2] == max_coste:
                return sol

    return valle(0, len(v))

def show_results(sol: Solution):
    print(f"{sol[0]} {sol[1]} {sol[2]}")


if __name__ == "__main__":
    v = read_data(sys.stdin)
    sol = process(v)
    show_results(sol)
