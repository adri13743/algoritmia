#!/usr/bin/env python3
import sys
from typing import TextIO

# Folleto en inglés es Leaflet
Leaflet = tuple[int, int, int]          # (num_folleto, anchura, altura)
LeafletPos = tuple[int, int, int, int]  # (num_folleto, num_hoja_de_imprenta, pos_x ,pos_y)

# Lee la instancia por la entrada estándar (ver apartado 1.1)
# Devuelve el tamaño del papel de la imprenta y la lista de folletos
def read_data(f: TextIO) -> tuple[int, list[Leaflet]]: #"""Comprobar que esto pasa los parámetros correctamente"""
    tamanyoPapel = int(f.readline())
    papelitos = []
    linea = [linea for linea in f.readlines()]
    for l in linea:
        aux = l.split()
        lf: Leaflet = (int(aux[0]), int(aux[1]), int(aux[2]))
        papelitos.append(lf)
    return tamanyoPapel, papelitos


# Recibe el tamaño del papel de la imprenta y la lista de folletos
# Devuelve tamaño del papel y lista de folletos
def process(paper_size: int, leaflet_list: list[Leaflet]) -> list[LeafletPos]:
    C = paper_size * paper_size #Area del papel grande
    contenedores: list[LeafletPos] = [] #Lista final que se quiere entregar
    indices = sorted(range(len(leaflet_list)), key=lambda i: -leaflet_list[i][1]) #Ordena los indices de leaflet_list para que coincidan con las areas
    lista_aux: list[list[int]] = [] #Contiene las h max y w max del papel grande y w auxiliar para colocar papelitos cuando no cabe más hacia arriba
    for i in indices:
        object = leaflet_list[i]    #Se van cogiendo los papelitos de la lista
        numFolleto = object[0]
        wObject = object[1]
        hObject = object[2]
        nc = None #Posible numero del contenedor
        for c in range(len(lista_aux)):
            wmax = lista_aux[c][0]
            hmax = lista_aux[c][1]
            waux = lista_aux[c][2]
            if (hmax + hObject <= paper_size and waux + wObject <= paper_size): #Cabe hacia arriba
                nc = c
                leafletpos: LeafletPos = (numFolleto, c + 1, waux, hmax)
                contenedores.append(leafletpos)
                lista_aux[c][1] += hObject
                break
            elif (wmax + wObject <= paper_size): #No cabe arriba y or lo tanto se prueba a la derecha
                nc = c
                lista_aux[c][0] += wObject
                leafletpos = (numFolleto, c + 1, wmax,0 )
                contenedores.append(leafletpos)
                lista_aux[c][1] += hObject
                break
        if nc is None: #Si no se ha podido añadir el papelito entonces
            aux: list[int] = [wObject,hObject,0] #w y h max cuando se crea un contenedor nuevo y w aux
            lista_aux.append(aux)  # Se añade a la lista que comparten el indice con las areas
            nc = len(lista_aux) - 1 #Cogemos la ubicación de este nuevo contenedor
            leafletpos = (numFolleto, nc + 1, 0, 0)
            contenedores.append(leafletpos)
    return contenedores #Aqui devolver contenedores
# Muestra por la salida estandar las posiciones de los folletos (ver apartado 1.2)
def show_results(leafletpos_list: list[LeafletPos]):
    for leaf in leafletpos_list:
        print(f"{leaf[0]} {leaf[1]} {leaf[2]} {leaf[3]}")
if __name__ == '__main__':
    paper_size0, leaflet_list0 = read_data(sys.stdin)
    leafletpos_list0 = process(paper_size0, leaflet_list0)
    show_results(leafletpos_list0)