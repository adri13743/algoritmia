#!/usr/bin/env python3
from traceback import print_tb

from easypaint import EasyPaint

from entregable2 import *
from entregable2_test import check_solution

def error_e(msg: str, e: Exception, tb):
    sys.stderr.write(f"ERROR: {msg}:\n  {e}")
    print_tb(tb, file=sys.stderr)
    sys.exit(1)


class ImprentaViewer(EasyPaint):
    def __init__(self,
                 page_size: int,
                 leaflet_dict: dict[int, tuple[int, int]],
                 leafletpos_list: list[LeafletPos]):
        super().__init__()
        self.sf = sf = 100
        self.page_size = page_size * sf

        self.leaflet_dict = {}
        for k, v in leaflet_dict.items():
            self.leaflet_dict[k] = v[0] * sf, v[1] * sf

        self.leafletpos_list = []
        for leaflet_id, page_id, px, py in leafletpos_list:
            if leaflet_id not in leaflet_dict:
                # sys.stderr.write(f"ERROR: El folleto {leaflet_id} no existe en la instancia. Se descarta.\n")
                continue
            self.leafletpos_list.append((leaflet_id, page_id, px * sf, py * sf))
        self.num_pages = max(s[1] for s in self.leafletpos_list)
        self.page = 1

    def on_key_press(self, keysym):
        if keysym == 'Right':
            self.page = self.page + 1 if self.page < self.num_pages else 1
        elif keysym == 'Left':
            self.page = self.page - 1 if self.page > 1 else self.num_pages
        elif keysym == 'Up':
            self.page = min(self.page + 100, self.num_pages)
        elif keysym == 'Down':
            self.page = max(self.page - 100, 1)
        elif keysym == 'Escape':
            self.close()
            return
        self.show_page(self.page)

    def show_page(self, page_id: int):
        self.erase()
        s = 2 * (self._right - self._left) / self._width
        self.create_filled_rectangle(-s, -s, self.page_size + s, self.page_size + s, "black")
        self.create_filled_rectangle(0, 0, self.page_size, self.page_size, "lightgrey")
        ocup = 0
        for f_id, x, y in ((s[0], s[-2], s[-1]) for s in self.leafletpos_list if s[1] == page_id):
            sx, sy = self.leaflet_dict[f_id]
            self.create_filled_rectangle(x, y, x + sx, y + sy, "black", "yellow")
            self.create_text(x + sx / 2, y + sy / 2, f"{f_id}", 6, anchor="S")
            self.create_text(x + sx / 2, y + sy / 2, f"{int(sx / self.sf)}x{int(sy / self.sf)}", 6, anchor="N")
            ocup += sx * sy
        for f_id, x, y in ((s[0], s[-2], s[-1]) for s in self.leafletpos_list if s[1] == page_id):
            sx, sy = self.leaflet_dict[f_id]
            self.create_rectangle(x, y, x + sx, y + sy, "black", dash=(6, 7))
        fo = 100 * ocup / self.page_size ** 2
        sep = 20 * (self._right - self._left) / self._width
        self.create_text(self.page_size / 2, -sep, f"Página {self.page} de {self.num_pages}", 20, anchor="N")
        self.create_text(-sep, self.page_size / 2, "←", 30, anchor="N")
        self.create_text(self.page_size + sep, self.page_size / 2, "→", 30, anchor="N")
        ps = int(self.page_size / self.sf)
        self.create_text(0, self.page_size + sep, f'Tamaño de página: {ps}x{ps}', 12, anchor="SW")
        self.create_text(self.page_size, self.page_size + sep, f'Ocupación: {fo:.2f} %', 12, anchor="SE")

    def main(self):
        m = self.page_size / 10
        self.easypaint_configure(title='Visor para el entregable2 - Teclas: ←, →, ↑, ↓, <esc>',
                                 background='white',
                                 size=(800, 800),
                                 coordinates=(-m, -m, self.page_size + m, self.page_size + m))
        self.page = 1
        self.show_page(self.page)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USO:\n\tpython3 entregable2_viewer.py <instancia_imprenta.i> ")
    else:
        print("Pasos:")
        print(f'  1. Leyendo el fichero de instancia {sys.argv[1]}...')
        try:
            with open(sys.argv[1]) as f:
                try:
                    page_size0, leaflet_list0 = read_data(f)
                except Exception as e:
                    tb = sys.exc_info()[2]
                    error_e("Tu función 'read_data()' ha lanzado una excepción", e, tb)
        except Exception as e:
            tb = sys.exc_info()[2]
            error_e(f"Al abrir el archivo {sys.argv[1]} se ha lanzado una excepción", e, tb)

        leaflet_dict0: dict[int, tuple[int, int]] = {}
        for n, width, height in leaflet_list0:
            leaflet_dict0[n] = width, height

        print(f'  2. Ejecutando tu process...')
        leafletpos_list: list[LeafletPos] = []
        try:
            leafletpos_list = process(page_size0, leaflet_list0)
        except Exception as e:
            tb = sys.exc_info()[2]
            error_e("Tu función 'process()' ha lanzado una excepción", e, tb)

        print(f'  3. Comprobando tu solución...')
        msg, num_pages = check_solution(page_size0, leaflet_list0, leafletpos_list)
        if msg != '':
            print(f"     ERROR: {msg}")

        print(f'  4. Lanzando el visor...')
        print("     " + "-" * 60)
        print("     CÓMO UTILIZAR EL VISOR:")
        print("     - Pon el foco del teclado en la ventana gráfica.")
        print("     - Muévete por las hojas de una en una con las fechas del cursor 'izquierda' y 'derecha'.")
        print("     - Muévete por las hojas de cien en cien con las fechas del cursor 'arriba' y 'abajo'.")
        print("     " + "-" * 60)
        input('     Pulsa <Return> para lanzar el visor: ')
        ImprentaViewer(page_size0, leaflet_dict0, leafletpos_list).run()
