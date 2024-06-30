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
            if v[centro] < min(v[l], v[r]): # Si hay valle
                h = min(v[l], v[r])
                d = r - l - 1
                coste = d * h - v[centro]
                return l, r, coste
            else:
                return 0, 1, 0
        c = (l + r) // 2
        sol_izq = valle(l, c)
        sol_der = valle(c, r)
        in_der = c+1
        aux_sum_der = 0
        sum_der = 0
        max_der = v[c+1]
        for k in range(c+1, r):# Lado derecho
            if v[k] < v[k + 1] and v[k+1] > max_der:
                sum_der += v[k]+aux_sum_der
                aux_sum_der = 0
                in_der = k + 1
                max_der = v[k+1]
            else:
                aux_sum_der+=v[k]
        in_izq = c
        aux_sum_izq = 0
        sum_izq = 0
        max_izq = v[c]
        for k in range(c, l, -1):# Lado izquierdo
            if v[k] < v[k - 1] and v[k-1] > max_izq:
                sum_izq += v[k]+aux_sum_izq
                aux_sum_izq = 0
                in_izq = k - 1
                max_izq = v[k-1]
            else:
                aux_sum_izq+=v[k]

        if max_izq < max_der:
            in_izq = c
            aux_sum_izq = 0
            sum_izq = 0
            max_izq = v[c]
            for k in range(c, l, -1):
                if v[k] < v[k - 1] and v[k - 1] <= max_der and v[k - 1] > max_izq:
                    sum_izq += v[k]
                    sum_izq += aux_sum_izq
                    aux_sum_izq = 0
                    in_izq = k - 1
                    max_izq = v[k - 1]
                else:
                    aux_sum_izq += v[k]
        elif max_izq > max_der:
            in_der = c
            aux_sum_der = 0
            sum_der = 0
            max_der = v[c+1]
            for k in range(c+1, r):
                if v[k] < v[k + 1] and v[k + 1] <= max_izq and v[k + 1] > max_der:
                    sum_der += v[k]
                    sum_der += aux_sum_der
                    aux_sum_der = 0
                    in_der = k + 1
                    max_der = v[k + 1]
                else:
                    aux_sum_der += v[k]

        h = min(v[in_izq], v[in_der])
        d = in_der - in_izq - 1
        coste_centro = d * h - (sum_izq + sum_der)
        sol_centro: Solution = (in_izq, in_der, coste_centro)
        max_coste = max(sol_izq[2], sol_centro[2], sol_der[2])
        lista_sol: list[Solution] = [sol_izq, sol_centro, sol_der]
        for solution in lista_sol:
            if max_coste == solution[2]:
                return solution

    return valle(0, len(v) - 1)

def show_results(sol: Solution):
    print(f"{sol[0]} {sol[1]} {sol[2]}")


if __name__ == "__main__":
    v = read_data(sys.stdin)
    sol = process(v)
    show_results(sol)