#!/usr/bin/env python3
import sys

if sys.version_info.major != 3 or sys.version_info.minor < 10:
    raise RuntimeError("This program needs Python3, version 3.10 or higher")

from io import StringIO
from time import process_time

from e1 import read_data, process, show_results


def error(msg: str):
    print("ERROR. " + msg, file=sys.stderr)
    exit()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage:\n  python3.10 e1_test.py <path_to_instance> <path_to_solution> <timeout (in seconds)>"
        )
        print(
            "Example:\n  python3.10 e1_test.py public_test/lab_000012.i public_test/lab_000012.o 1"
        )
        exit(-100)

    instance_fn, solution_fn, timeout = sys.argv[1], sys.argv[2], int(sys.argv[3])

    # Utilizar read_data() --------------
    rows = cols = -1
    try:
        with open(instance_fn) as f:
            try:
                g, rows, cols = read_data(f)
            except Exception as e:
                error(
                    f"Tu función read_data() ha lanzado una excepción al leer el archivo '{instance_fn}':\n\t"
                    + str(e)
                )
    except Exception as e:
        error(f"Excepción al leer el archivo '{instance_fn}':\n\t" + str(e))

    try:
        with open(solution_fn) as f:
            solution = int(f.readline())
    except Exception as e:
        error(f"Excepción al leer el archivo '{solution_fn}':\n\t" + str(e))

    # Utilizar process() --------------
    result = -1
    cpu_time = -1
    is_correct = is_in_time = False
    t0 = process_time()
    try:
        result = process(g, rows, cols)
    except Exception as e:
        error(f"Tu función 'process()' ha lanzado una excepción:\n\t" + str(e))
    cpu_time = process_time() - t0
    is_in_time = cpu_time <= timeout
    is_correct = result == solution

    # Utilizar show_results() --------------
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    out_txt = ""
    try:
        show_results(result)
        out_txt = mystdout.getvalue().strip()
    except Exception as e:
        error(f"Tu función 'show_results()' ha lanzado una excepción:\n\t" + str(e))
    finally:
        sys.stdout = old_stdout
    if out_txt != str(solution):
        error(f"La salida de 'show_results()' no es correcta:\n" + out_txt)

    # MOSTRAR RESULTADO DE process() --------------
    if is_correct:
        if is_in_time:
            print(f"SOLUTION OK - TIME OK ({cpu_time:.4f} sec)")
        else:
            print(f"SOLUTION OK - TIME ERROR ({cpu_time:.4f} sec)")
    else:
        if is_in_time:
            print(f"SOLUTION ERROR - TIME OK ({cpu_time:.4f} sec)")
        else:
            print(f"SOLUTION ERROR - TIME ERROR ({cpu_time:.4f} sec)")
