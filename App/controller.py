"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import time
import csv
import tracemalloc
from DISClib.ADT import list as lt
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
muestra="10-por"

def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = model.new_data_structs()
    return control

# Funciones para la carga de datos
def cantidad_datos(cant):
    model.cantidad_datos(cant)
    
def printjobtab(csv):
    jobs=model.printjobtab(csv)
    return(jobs)

def load_data(control):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    jobs = loadjobs(control)
    skills = loadskills(control)
    multilocations = loadMulti(control)
    employments = loadEmployment(control)
    jobs = model.add_infojob(control)
    jobs = sort(control)
    for job in range(lt.size(jobs)):
        arbol_fechas = model.add_fecha(control,lt.getElement(jobs,job))
        arbol_salarios = model.add_salario(control,lt.getElement(jobs,job))
    return jobs,skills,multilocations, employments,arbol_fechas, arbol_salarios

def loadjobs(control):
    global muestra
    booksfile = cf.data_dir + muestra+"-jobs.csv"
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'),delimiter=";")
    for job in input_file:
        model.add_job(control, job)
        
        
def loadskills(control):
    booksfile = cf.data_dir + muestra + "-skills.csv"
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'),delimiter=";")
    for skill in input_file:
        model.add_skills(control, skill)
        
def loadMulti(control):
    global muestra
    booksfile = cf.data_dir + muestra+"-multilocations.csv"
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'),delimiter=";")
    for multi in input_file:
        model.add_multi(control, multi)
        
def loadEmployment(control):
    global muestra
    booksfile = cf.data_dir + muestra+"-employments_types.csv"
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'),delimiter=";")
    for employ in input_file:
        model.add_employ(control, employ)

# Funciones de ordenamiento
def data_size(data):
    size=model.data_size(data)
    return(size)
def data_sizem(data):
    size=model.data_sizem(data)
    return(size)
def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    starttime=get_time()
    control=model.sort(control["jobs"])
    endtime=get_time()
    delta=delta_time(starttime,endtime)
    return(control)


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(control):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
