#!/usr/bin/env python3

import io
from contextlib import redirect_stdout
from enum import Enum
from time import process_time
from traceback import print_tb

from entregable2 import *


class Result(Enum):
    OK = 1
    ERROR_USEDPAGES = 2
    ERROR_TIMEOUT = 3
    ERROR_INVALID_SOLUTION = 4
    ERROR_EXCEPTION_LAUNCHED = 5
    ERROR_CHECK_FAILED = 6


def error(msg: str):
    print(f"RESULT: {Result.ERROR_CHECK_FAILED}")
    print(f"  ERROR: {msg}")
    sys.exit(1)


def error_e(msg: str, e: Exception, tb):
    print(f"RESULT: {Result.ERROR_EXCEPTION_LAUNCHED.name}")
    print(f"  ERROR: {msg}")
    print(f'         {e}\n')
    sys.stderr.write(f'{"-" * 20}\n')
    print_tb(tb, file=sys.stderr)
    sys.stderr.write(f'{"-" * 60}\n')
    sys.exit(1)


def print_debug(msg: str):
    # sys.stderr.write(msg + '\n')  # Descomentar para depuración
    return


def check_show_results_output(leafletpos_list: list[LeafletPos]):
    print_debug(f"Ejecutando tu 'show_results()'...")
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            show_results(leafletpos_list)
        except Exception as e:
            tb = sys.exc_info()[2]
            error_e(f"Tu función 'show_results()' ha lanzado una excepción", e, tb)
        lines: list[str] = f.getvalue().strip().split('\n')

    print_debug(f"Comprobando la salida de 'show_results()'...")
    i = 0
    for line in lines:
        i += 1
        current_line = line
        try:
            _1, _2, _3, _4 = [int(e) for e in line.split()]
        except Exception as e:
            tb = sys.exc_info()[2]
            error_e(f"Al analizar la línea {i} de tu salida ('{current_line}') se ha lanzado una excepción", e, tb)


def get_read_data(filename: str) -> tuple[int, list[Leaflet]]:
    print_debug(f"Ejecutando tu 'read_data()'...")
    page_size0 = 0
    leaflet_list0 = []
    try:
        with open(filename) as f:
            lines = f.readlines()
        try:
            page_size0 = int(lines[0])
            leaflet_list0 = [tuple(int(e) for e in line.split()) for line in lines[1:]]
        except Exception:
            error(f"El archivo '{filename}' no tiene el formato adecuado")
    except Exception as e:
        tb = sys.exc_info()[2]
        error_e(f"Al abrir el archivo '{filename}' se ha lanzado una excepción", e, tb)

    with open(filename) as f:
        try:
            page_size, leaflet_list = read_data(f)
        except Exception as e:
            tb = sys.exc_info()[2]
            error_e(f"Tu función 'read_data()' ha lanzado una excepción", e, tb)

    if page_size0 != page_size:
        error(f"Tu read_data() ha devuelto un tamaño de hoja erroneo")
    if leaflet_list0 != leaflet_list:
        error(f"Tu read_data() ha devuelto una lista de folletos erronea")
    return page_size, leaflet_list


def get_process_output(page_size, leaflet_list) -> tuple[list[LeafletPos], float]:
    print_debug(f"Ejecutando tu 'process()'...")
    leafletpos_list: list[LeafletPos] = []
    elapsed_time: float = 0
    try:
        t0 = process_time()
        leafletpos_list = process(page_size, leaflet_list)
        t1 = process_time()
        elapsed_time = t1 - t0
    except Exception as e:
        tb = sys.exc_info()[2]
        error_e(f"Tu función 'process()' ha lanzado una excepción", e, tb)
    return leafletpos_list, elapsed_time


def check_solution(page_size: int,
                   leaflet_list: list[Leaflet],
                   leafletpos_list: list[LeafletPos]) -> tuple[str, int]:
    Rectangle = tuple[int, int, int, int]  # x, y, ancho, alto

    def solapa(r1: Rectangle, r2: Rectangle) -> bool:
        x1, y1, w1, h1 = r1
        x2, y2, w2, h2 = r2
        return (x1 <= x2 < x1 + w1 or x2 <= x1 < x2 + w2) and \
               (y1 <= y2 < y1 + h1 or y2 <= y1 < y2 + h2)

    def rectangulo(x: int, y: int, w: int, h: int) -> Rectangle:
        # return pos[2], pos[3], folleto[2], folleto[3]  #BUG
        return x, y, w, h

    print_debug(f'Comprobando la solución...')

    pages_ids = set(f[1] for f in leafletpos_list)
    for page_id in range(1, len(pages_ids) + 1):
        if page_id not in pages_ids:
            return f"Hoja sin folletos: {page_id}", -1

    leaflet_dict = dict((f[0], (f[1], f[2])) for f in leaflet_list)
    leafletpos_dict = dict((f[0], (f[1], f[2], f[3])) for f in leafletpos_list)
    for f_id in leaflet_dict:
        f_w, f_h = leaflet_dict[f_id]
        if f_id not in leafletpos_dict:
            return f"Falta folleto en solución: El folleto {f_id} ({f_w}x{f_h}) no aparece en ninguna hoja", -1
    for f_id in leafletpos_dict:
        if f_id not in leaflet_dict:
            return f"Folleto desconocido en la hoja {leafletpos_dict[f_id][0]}: {f_id}", -1

    pages = {}
    for folleto_pos in leafletpos_list:
        page_id = folleto_pos[1]
        pages.setdefault(page_id, []).append(folleto_pos)

    for page_id, folletos_pos in pages.items():
        for ii, folleto_pos in enumerate(folletos_pos):
            f_id, _, px, py = folleto_pos
            f_w, f_h = leaflet_dict[f_id]
            r = rectangulo(px, py, f_w, f_h)
            if px < 0 or px + f_w > page_size or py < 0 or py + f_h > page_size:
                return f"Folleto fuera de límites: {f_id} ({f_w}x{f_h}) en pos {(px, py)} de hoja {page_id}", -1
            for j in range(ii + 1, len(folletos_pos)):
                f_id2, page_id2, px2, py2 = folletos_pos[j]
                f_w2, f_h2 = leaflet_dict[f_id2]
                r2 = rectangulo(px2, py2, f_w2, f_h2)
                if solapa(r, r2):
                    return f"Folletos solapados en la hoja {page_id}: {f_id} ({f_w}x{f_h}) en pos {(px, py)} y {f_id2} ({f_w2}x{f_h2}) en pos {(px2, py2)}", -1

    return '', len(pages)


def check_instance(filename) -> Result:
    print(f"INSTANCE: {filename}")

    page_size, leaflet_list = get_read_data(filename)  # Puede lanzar excepción

    max_seconds = 3
    max_pages = int(filename[:-2].split('_')[-1])

    leafletpos_list, elapsed_time = get_process_output(page_size, leaflet_list)  # Puede lanzar excepción

    # Comprobar la solución devuelta por tu process()
    primer_error, np = check_solution(page_size, leaflet_list, leafletpos_list)  # Puede lanzar excepción

    if primer_error == '':
        # Comprobar la salida de tu show_results()
        check_show_results_output(leafletpos_list)  # Puede lanzar excepción
        if elapsed_time <= max_seconds and np <= max_pages:
            print(f"RESULT: {Result.OK.name}")
            print(f"  NUMPAGES: OK - {np} pages (<= {max_pages} pages)")
            print(f"  USEDTIME: OK - {elapsed_time:.2f} sec (<= {max_seconds} sec)")
            return Result.OK
        elif np > max_pages:
            print(f"RESULT: {Result.ERROR_USEDPAGES.name}")
            print(f"  NUMPAGES: ERROR - {np} pages (> {max_pages} pages)")
            if elapsed_time <= max_seconds:
                print(f"  USEDTIME: OK - {elapsed_time:.2f} sec (<= {max_seconds} sec)")
            else:
                print(f"  USEDTIME: ERROR - {elapsed_time:.2f} sec (> {max_seconds} sec)")
        else:
            print(f"RESULT: {Result.ERROR_TIMEOUT.name}")
            print(f"  NUMPAGES: OK - {np} pages (<= {max_pages} pages)")
            print(f"  USEDTIME: ERROR - {elapsed_time:.2f} sec (> {max_seconds} sec)")
            return Result.ERROR_TIMEOUT
    else:
        print(f"RESULT: {Result.ERROR_INVALID_SOLUTION.name}")
        print(f"  {primer_error}")
        return Result.ERROR_INVALID_SOLUTION


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Ejemplo de uso: python3.10 entregable2_test.py <file1.i> <file2.i> ... ")
        sys.exit(1)

    print('-' * 60)
    for fn in sys.argv[1:]:
        check_instance(fn)
        print('-' * 60)
