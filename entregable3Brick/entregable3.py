from __future__ import annotations

import sys
import direction
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Optional, TextIO

from algoritmia.schemes.bt_scheme import bt_min_solve, ScoredDecisionSequence

from board import Board, RowCol
from brick import Brick
from direction import Direction, directions2string

# Variable global con la salida de show_results() si no hay solución
INSTANCE_WITHOUT_SOLUTION = "INSTANCE WITHOUT SOLUTION"

# Tipos que utilizarás en el process() al aplicar el esquema de backtracking
Decision = Direction  # Cuatro valores posibles: Directions.Right, Direction.Left, Direction.Up, Direction.Down
Solution = tuple[Decision, ...]  # Utilizad la función auxiliar 'directions2string' de direction.py para convertir
                                 # una solución en una cadena del tipo 'RRUUULLDR...'
Score = int
State = Brick

@dataclass
class Extra:
    b: brick

# ---------------------------------------------------------------------------------------------------------------------

def read_data(f: TextIO) -> Board:
    my_board = Board(f.readlines())
    return my_board


def process(board: Board) -> Optional[Solution]:
    class BrickDS(ScoredDecisionSequence):
        def is_solution(self) -> bool:
            return self.extra.b.b1 == board.target_pos() and self.extra.b.b2 == board.target_pos()

        def solution(self) -> Solution:
            return self.decisions()

        def score(self) -> Score:
            return len(self)

        def state(self) -> State:
            return self.extra.b

        def successors(self) -> Iterator[BrickDS]:
            if not self.is_solution():
                for mov in Direction:
                    copia_brick: Brick = self.extra.b.move(mov)
                    if board.has_tile(copia_brick.b1) and board.has_tile(copia_brick.b2):
                        yield self.add_decision(mov, Extra(copia_brick))

    pos_camino: int = 0
    if board.has_tile(RowCol(board.target_pos().row + 1, board.target_pos().col)) or board.has_tile(
            RowCol(board.target_pos().row, board.target_pos().col + 1)) or board.has_tile(
            RowCol(board.target_pos().row - 1, board.target_pos().col)) or board.has_tile(
            RowCol(board.target_pos().row, board.target_pos().col - 1)):
        pos_camino += 1
    if pos_camino == 0:
        return None

    lista: list[Solution] = list(bt_min_solve(BrickDS(Extra(Brick(board.start_pos(), board.start_pos())))))
    if len(lista) > 0:
        return lista[-1]
    else:
        None


def show_results(solution: Optional[Solution]):
    if solution is None:
        print(INSTANCE_WITHOUT_SOLUTION)
    else:
        res = direction.directions2string(solution)
        print(res)


# Programa principal --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    board0 = read_data(sys.stdin)
    solution0 = process(board0)
    show_results(solution0)