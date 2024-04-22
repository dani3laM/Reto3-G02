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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

from tabulate import tabulate
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
#from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import bst as bst
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf
from datetime import datetime

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    catalog= {"jobs": None,
              "employments": None,
              "multilocations": None,
              "skills": None,
              'fechas':None,
              'salarios':None}
    
    catalog['jobs']=lt.newList('ARRAY_LIST', comp_by_id)
    catalog['employments'] = mp.newMap(maptype='CHAINING',cmpfunction=comp_by_id)
    catalog['multilocations'] = mp.newMap(maptype='CHAINING',cmpfunction=comp_by_id)
    catalog['skills'] = mp.newMap(maptype='CHAINING',cmpfunction=comp_by_id)
    catalog['fechas'] = om.newMap(omaptype='BST',cmpfunction=compareDates)
    catalog['salarios'] = om.newMap(omaptype='BST',cmpfunction=comparesalary)
    
    return catalog
def comparesalary(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def comp_by_id(id1, id2)->int:
    caso1 = isinstance(id1, dict)
    caso2 = isinstance(id2, dict)
    if caso1 or caso2:
        pass
    else:
        if (id1 == id2["value"]["id"]):
            return 0
        elif id1 > id2["value"]["id"]:
            return 1
        else:
            return -1
# Funciones para agregar informacion al modelo

def add_job(catalog, job):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    job['skills'] = lt.newList('SINGLE_LINKED', comp_by_id)
    job['salario']= None
    job['ubicaciones'] = lt.newList('SINGLE_LINKED', comp_by_id)
    job = time(job)
    lt.addLast(catalog['jobs'], job)
    return catalog


# Funciones para creacion de datos
def time(job):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    
    date_format="%Y-%m-%dT%H:%M:%S.%fZ"
    
    date = job['published_at']
    
    new_date = datetime.strptime(date, date_format)
    
    job['published_at'] = new_date
    
    return job
def add_fecha(catalog,job):
    fecha = job['published_at']
    if fecha is not None:
        hay = om.get(catalog['fechas'],fecha)
        if hay is None:
            lista = lt.newList('ARRAY_LIST', comp_by_id)
            lt.addLast(lista,job)
            om.put(catalog['fechas'],fecha,lista)
        else:
            lista = me.getValue(hay)
            lt.addLast(lista,job)
    return catalog

def add_salario(catalog,job):
    salario = job['salario']
    if salario is not None:
        hay = om.get(catalog['salarios'],salario)
        if hay is None:
            lista = lt.newList('ARRAY_LIST', comp_by_id)
            lt.addLast(lista,job)
            om.put(catalog['salarios'],salario,lista)
        else:
            lista = me.getValue(hay)
            lt.addLast(lista,job) 
    return catalog  

def add_skills(catalog,skill):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    id = skill['id']
    #print(catalog['skills'])
    hay = mp.get(catalog['skills'],id)
    if hay is None:
        lista = lt.newList('ARRAY_LIST', comp_by_id)
        lt.addLast(lista,skill['name'])
        mp.put(catalog['skills'], id, lista)
    else:
        lista = me.getValue(hay)
        lt.addLast(lista,skill['name'])
    return catalog

def add_multi(catalog,multi):
    id = multi['id']
    hay = mp.get(catalog['multilocations'],id)
    if hay is None:
        lista = lt.newList('SINGLE_LINKED', comp_by_id)
        lt.addLast(lista,multi['city'])
        mp.put(catalog['multilocations'], id, lista)
    else:
        lista = me.getValue(hay)
        lt.addLast(lista,multi['city'])  
    return catalog
   
def add_employ(catalog,employ):
    id = employ['id']
    hay = mp.get(catalog['employments'],id)
    if hay is None:
        mp.put(catalog['employments'], id, employ['salary_from'])
    else:
        lista = me.getValue(hay)
        lt.addLast(lista,employ['salary_from'])  
    return catalog 

def add_infojob(catalog):
    for i in range(lt.size(catalog['jobs'])):
        job = lt.getElement(catalog['jobs'],i)
        ids = job['id']
        skill = mp.get(catalog['skills'],ids)
        multi = mp.get(catalog['multilocations'],ids)
        employ = mp.get(catalog['employments'],ids)
        if skill is not None:
            newskill = me.getValue(skill)
            lt.addLast[job['skills'],newskill]
        if multi is not None:
            newlocation = me.getValue(multi)
            lt.addLast[job['ubicaciones'],newlocation]
        if employ is not None:
            newvalor = me.getValue(employ)
            job['pago'] = newvalor    
    return job
            
def printjobtab(csv):
    jobs=csv
    diccionario=lt.newList(datastructure="ARRAY_LIST",cmpfunction=comp_by_id)
    for i in range(lt.size(jobs)):
        diccio={"published_at": jobs["elements"][i]["published_at"],
                "title": jobs["elements"][i]["title"],
                "company_name": jobs["elements"][i]["company_name"],
                "experience_level": jobs["elements"][i]["experience_level"],
                "country_code": jobs["elements"][i]["country_code"],
                "city": jobs["elements"][i]["city"]}
        lt.addLast(diccionario,diccio)
    global canti
    jobsfal=[]
    first= lt.subList(diccionario,1,(canti//2))
    last= lt.subList(diccionario,int(lt.size(diccionario)-((canti//2)-1)),(canti//2))
    jobshead=diccionario
    jobsfirst=lt.firstElement(jobshead)
    headers= list(jobsfirst.keys())
    for elements in lt.iterator(first):
        jobsfal.append(elements.values())
    for elements in lt.iterator(last):
        jobsfal.append(elements.values())
    tab=(tabulate(jobsfal,headers=headers,tablefmt="pretty"))
    return(tab)
canti=6

def cantidad_datos(cant):
    global canti
    canti=cant
    
# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data):
    size= lt.size(data)
    return(size)

def data_sizem(data):
    size= mp.size(data)
    return(size)

def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    return(data_1["published_at"]<data_2["published_at"])


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    sorted=(merg.sort(data_structs,sort_criteria))
    return sorted
