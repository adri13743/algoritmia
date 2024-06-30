#!/usr/bin/env python3
import sys

if sys.version_info.major != 3 or sys.version_info.minor < 10:
    raise RuntimeError("This program needs Python3, version 3.10 or higher")

from algoritmia.viewers.labyrinth_viewer import LabyrinthViewer

from e1 import read_data


if __name__ == "__main__":
    g, rows, cols = read_data(sys.stdin)
    LabyrinthViewer(g, canvas_width=1400, canvas_height=800, wall_width=1).run()
