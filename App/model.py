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
              "jobsmapa":None,
              'skills': None,
              'fechas':None,
              'salarios':None}
    
    catalog['jobs']=lt.newList('ARRAY_LIST', comp_by_id)
    catalog['employments'] = mp.newMap(34500,
                                  maptype='PROBING',
                                  loadfactor=0.5,
                                  cmpfunction=comp_by_id)
    catalog['jobsmapa'] = mp.newMap(34500,
                                  maptype='PROBING',
                                  loadfactor=0.5,
                                  cmpfunction=comp_by_id)
    catalog['multilocations'] = mp.newMap(34500,
                                  maptype='PROBING',
                                  loadfactor=0.5,
                                  cmpfunction=comp_by_id)
    catalog['skills'] = mp.newMap(34500,
                                  maptype='PROBING',
                                  loadfactor=0.5,
                                  cmpfunction=comp_by_id)
    catalog['fechas'] = om.newMap(omaptype='BST',cmpfunction=compareDates)
    catalog['salarios'] = om.newMap(omaptype='BST',cmpfunction=comparesalary)
    
    return catalog
def comparesalary(date1, date2):
    """
    Compara dos fechas
    """
    date1 = int(date1)
    date2 = int(date2)
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
    
    #datetime.strptime(date1, date_format)
    #datetime.strptime(date2, date_format)
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
    job['salario']= 0
    id = job['id']
    job['ubicaciones'] = lt.newList('ARRAY_LIST', comp_by_id)
    job['skills'] = lt.newList('ARRAY_LIST', comp_by_id)
    job = time(job)
    lt.addLast(catalog['jobs'], job)
    #mp.put(catalog["jobsmapa"],id,job)
    hay = om.get(catalog['fechas'],job['published_at'])
    if hay is None:
        entry = lt.newList('SINGLE_LINKED', comp_by_id)
        lt.addLast(entry, job)
        om.put(catalog['fechas'], job['published_at'], entry)
    else:
        entry = me.getValue(hay)
        lt.addLast(entry,job)
        me.setValue(hay,entry)
    
        
        
    #return catalog['jobs']


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


def add_skills(catalog,skill):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    
    id = skill['id']
    #id = id.rstrip()
    #id = id.replace('\n','')
    #print(id)
    ha = mp.contains(catalog['skills'],id)
    if not ha:
        lista = lt.newList('ARRAY_LIST', comp_by_id)
        lt.addLast(lista,skill['name'])
        mp.put(catalog['skills'], id, lista)
    else:
        lista = me.getValue(ha)
        lt.addLast(lista,skill['name'])
        me.setValue(ha,lista)
    """"job = mp.get(catalog['jobsmapa'],id)
    print(job)
    print(id)
    if job is None:
        print(1)
    elif 'skills' not in job:
        lista = lt.newList('ARRAY_LIST', comp_by_id)
        job['skills'] = lista
    else:
        lista = job['skills']
    lt.addLast(lista,skill['name'])"""
    #return catalog['skills']

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
        me.setValue(hay,lista)
    #return catalog
   
def add_employ(catalog,employ):
    id = employ['id']
    if employ['salary_from'] == '':
        employ['salary_from'] = 0
        salario = employ['salary_from']
    else:
        salario = int(employ['salary_from'])
    """"job = mp.get(catalog['jobsmapa'],id)['value']
    job['salario'] = salario
    if hay is None:
        mp.put(catalog['employments'], id, salario)"""
    haysal = om.get(catalog['salarios'],salario)
    if haysal is None:
        lista = lt.newList('ARRAY_LIST', comp_by_id)
        lista = lt.addLast(lista,id)
        om.put(catalog['salarios'],salario,lista)
    else:
        #print(haysal)
        lista = me.getValue(haysal)
        if lista is None:
            lista = lt.newList('ARRAY_LIST', comp_by_id)
        lt.addLast(lista,id)
        me.setValue(haysal,lista)
    
    
    #return catalog['employments']

def add_infojob(catalog):
    for job in lt.iterator(catalog['jobs']):
        ids = job['id']
        #print(ids)
        skill = mp.get(catalog['skills'],ids)
        #print(skill)
        multi = mp.get(catalog['multilocations'],ids)
        employ = mp.get(catalog['employments'],ids)
        print('entre')
        
        if not skill is None:
                print(1)
                newskill = me.getValue(skill)
                job['skills'] = newskill
        if multi is not None:
                newlocation = me.getValue(multi)
                lt.addLast(job['ubicaciones'],newlocation['elements'])
        if  employ != None:
                newvalor = me.getValue(employ)
                if newvalor != '' and newvalor != ' ':
                    job['salario'] = newvalor    
    #return catalog
            
def printjobtab(jobs):
    diccionarios=lt.newList(datastructure="ARRAY_LIST",cmpfunction=comp_by_id)
    for i in range(lt.size(jobs)):
        job = lt.getElement(jobs,i)
        diccio={"published_at": job["published_at"],
                "title": job["title"],
                "company_name": job["company_name"],
                "experience_level": job["experience_level"],
                "country_code": job["country_code"],
                "city": job["city"],
                'skills':job['skills']['elements']}
        lt.addLast(diccionarios,diccio)
    global canti
    jobsfal=[]
    if lt.size(diccionarios) >= 10:
        first= lt.subList(diccionarios,1,5)
        last= lt.subList(diccionarios,int(lt.size(diccionarios)-4),5)
        """"jobshead=diccionarios"""
        jobsfirst=lt.firstElement(diccionarios)
        headers= list(jobsfirst.keys())
        for elements in lt.iterator(first):
            jobsfal.append(elements.values())
        for elements in lt.iterator(last):
            jobsfal.append(elements.values())
        tab=(tabulate(jobsfal,headers=headers,tablefmt="pretty"))
    else: 
        tab=(tabulate(diccionarios,headers=headers,tablefmt="pretty"))
    return tab
canti=6

def printlasttab(csv,num):
    if num>lt.size(csv):
        num=lt.size(csv)
    jobsfal=[]
    last= lt.subList(csv,int(lt.size(csv)-(num-1)),(num))
    jobs=csv
    jobsfirst=lt.firstElement(jobs)
    headers= list(jobsfirst.keys())
    
    for elements in lt.iterator(last):
        
        jobsfal.append(elements.values())
    tab=(tabulate(jobsfal,headers=headers,tablefmt="pretty"))
    return(tab)
def printfulltab(csv):
    jobsfal=[]
    jobs=csv
    jobsfirst=lt.firstElement(jobs)
    headers= list(jobsfirst.keys())
    
    for elements in lt.iterator(csv):
        
        jobsfal.append(elements.values())
    tab=(tabulate(jobsfal,headers=headers,tablefmt="pretty"))
    return(tab)

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

def req_1(data_structs,fechaini,fechafin):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    valores = om.values(data_structs['fechas'],fechaini,fechafin)
    #listaids = lt.newList(datastructure="ARRAY_LIST",cmpfunction=comp_by_id)
    respuesta = lt.newList(datastructure="ARRAY_LIST",cmpfunction=comp_by_id)
    for a in range(lt.size(valores)):
        lista = lt.getElement(valores,a)
        if lt.size(lista) == 1:
            lt.addLast(respuesta,lt.getElement(lista,1))
        else:
            for b in range(lt.size(lista)):
                lt.addLast(respuesta,lt.getElement(lista,b))
    return respuesta
                    
""""def tabreq(resultado):
    llaves = {'title','city','country_code','workplace_type','company_name','company_size','experience_level','published_at','id'}
    if lt.size(resultado) > 10"""
        


def req_2(control):
    pass


def req_3(control,pais,nivel):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    cant=0
    ofertas=lt.newList(datastructure="ARRAY_LIST",cmpfunction=comp_by_id)
    jobs=control["jobs"]
    for i in range(lt.size(jobs)):
        try:
            if jobs["elements"][i]["country_code"].lower()==pais.lower() and jobs["elements"][i]["experience_level"].lower()==nivel.lower():
                diccio={"published_at": jobs["elements"][i]["published_at"],
                        "title": jobs["elements"][i]["title"],
                        "company_name": jobs["elements"][i]["company_name"],
                        "experience_level": jobs["elements"][i]["experience_level"],
                        "country_code": jobs["elements"][i]["country_code"],
                        "city": jobs["elements"][i]["city"],
                        "company_size": jobs["elements"][i]["company_size"],
                        "workplace_type": jobs["elements"][i]["workplace_type"],
                        "open_to_hire_ukrainians": jobs["elements"][i]["open_to_hire_ukrainians"],
                        "id": jobs["elements"][i]["id"]}
                lt.addLast(ofertas,diccio)
                cant+=1
        except Exception as e:
            diccio={"published_at": 0,
                        "title": 0,
                        "company_name": 0,
                        "experience_level": 0,
                        "country_code": 0,
                        "city": 0,
                        "company_size": 0,
                        "workplace_type": 0,
                        "open_to_hire_ukrainians": 0,
                        "id":0}
            lt.addLast(ofertas,diccio)
    try:
        1/cant
    except Exception as e:
        print("No se encontraron ofertas de trabajo que cumplan con el pais y nivel de experticia")
        diccio={"published_at": 0,
                    "title": 0,
                    "company_name": 0,
                    "experience_level": 0,
                    "country_code": 0,
                    "city": 0,
                    "company_size": 0,
                    "workplace_type": 0,
                    "open_to_hire_ukrainians": 0,
                    "id":0}
        lt.addLast(ofertas,diccio)
    return(ofertas)
    


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


def req_6(control,num,fechaini,fechafin,salarioini,salariofin):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    valoressalario = om.values(control['salarios'],salarioini,salariofin)
    valoresfecha = om.values(control['fechas'],fechaini,fechafin)
    respuesta = lt.newList(datastructure="ARRAY_LIST",cmpfunction=comp_by_id)
    listasalario = lt.newList(datastructure="ARRAY_LIST",cmpfunction=comp_by_id)
    listafecha = lt.newList(datastructure="ARRAY_LIST",cmpfunction=comp_by_id)
    """for a in range(lt.size(valoressalario)):
        lista = lt.getElement(valoressalario,a)
        if lt.size(lista) == 1:
            lt.addLast(listasalario,lt.getElement(lista,1))
        else:
            for b in range(lt.size(lista)):
                lt.addLast(listasalario,lt.getElement(lista,b))"""
        
    for a in range(lt.size(valoresfecha)):
        lista = lt.getElement(valoresfecha,a)
        for b in range(lt.size(lista)):
            if lt.getElement(lista,b):
                lt.addLast(listafecha,lt.getElement(lista,b))
    if lt.size(listafecha) >= lt.size(listasalario):
        respuesta = listasalario
    else:
        respuesta = listafecha
    numerojobs = lt.size(respuesta)
    ciudades = {}
    for job in lt.iterator(respuesta):
        ciudad = job['city']
        if ciudad in ciudades:
            lt.addLast(ciudades[ciudad],job)
        else:
            ciudades[ciudad] = lt.newList(datastructure="ARRAY_LIST",cmpfunction=comp_by_id)
    
        

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
