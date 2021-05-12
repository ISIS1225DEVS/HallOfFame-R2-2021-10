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
import csv
import time
import tracemalloc
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de videos


def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog


# Funciones para la carga de datos


def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos, a su vez mide el tiempo de ejecución
    """
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    loadVideos(catalog)
    loadCategories(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory


def loadVideos(catalog):
    """
    Carga los videos del archivo.
    """
    videosfile = cf.data_dir + 'videos/videos-large.csv'
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video)


def loadCategories(catalog):
    """
    Carga todas las categorías del archivo y los agrega a la lista de
    categorias
    """
    categoriesfile = cf.data_dir + 'videos/category-id.csv'
    input_file = csv.DictReader(
        open(categoriesfile, encoding='utf-8'), delimiter='\t')
    for category in input_file:
        model.addCategory(catalog, category)


# Funciones de consulta sobre el catálogo


def videosSize(catalog):
    """
    Numero de videos cargados al catalogo
    """
    return model.videosSize(catalog)


def categoriesSize(catalog):
    """
    Numero de videos cargados al catalogo
    """
    return model.categoriesSize(catalog)


def countriesSize(catalog):
    """
    Numero de videos cargados al catalogo
    """
    return model.countriesSize(catalog)


def getVideosByCountry(catalog, country):
    '''
    Retorna los videos de un país específico
    '''
    return model.getVideosByCriteriaMap(catalog, 'country', country)


def getMostTrendingDaysByID(catalog):
    '''
    Retorna los videos que más tiempo fueron tendencia
    '''
    sorted_videos = model.sortVideos(
        catalog, lt.size(catalog), 'comparetitles')
    result = model.getMostTrendingDaysByID(sorted_videos[1])
    return result


def getVideosByCategory(catalog, category):
    '''
    Retorna los videos de una categoría específica
    '''
    return model.getVideosByCriteriaMap(catalog, 'category', category)


def getVideosByCountryAndTag(catalog, tag, country):
    '''
    Retorna los videos de un país y tag específicos
    '''
    return model.getVideosByCountryAndTag(catalog, tag, country)


def getVideosByCategoryAndCountry(catalog, category, country):
    '''
    Retorna los videos dado un país y categoría específicos
    '''
    return model.getVideosByCategoryAndCountry(catalog, category, country)


# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
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
