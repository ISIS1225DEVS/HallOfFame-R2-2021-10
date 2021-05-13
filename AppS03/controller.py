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
import time
import tracemalloc
import config as cf
import model
import csv



# ======================================
# Inicialización del Catálogo de libros
# ======================================



def initCatalog():

    catalog = model.newCatalog()
    return catalog



# ================================
# Funciones para la carga de datos
# ================================



def loadData(catalog):
    
    tracemalloc.start()
    
    delta_time = -1.0
    delta_memory = -1.0

    start_time = getTime()
    start_memory = getMemory()

    loadCategories(catalog)
    loadVideos(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory

    
def loadVideos(catalog):

    videosfile = cf.data_dir + 'videos/videos-large.csv'
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video)
        model.addCategorySorted(catalog, video)
        model.addCountriesSorted (catalog, video)
        model.addCountryCategorySorted (catalog, video)


def loadCategories(catalog):

    categoriesfile = cf.data_dir + 'videos/category-id.csv'
    input_file = csv.DictReader(open(categoriesfile, encoding='utf-8'),delimiter='\t')
    for category in input_file:
        model.addCategory(catalog, category)



# ==========================
# Funciones de ordenamiento
# ==========================



def sortVideosByViews(catalog, category, country):
    
    return model.sortVideosByViews(catalog, category, country)



# =======================================
# Funciones de consulta sobre el catálogo
# =======================================



def firstVideo(catalog):

    firstvideo = model.firstVideo(catalog)

    return firstvideo


def sortVideosCountryTrending (catalog,country):

    return model.sortVideosCountryTrending (catalog, country)


def sortVideosLikesTag(catalog, tag, country):

    return model.sortVideosLikesTag(catalog, tag, country)


def sortVideosCategoryTrending (catalog, category):

    return model.sortVideosCategoryTrending (catalog, category)



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


    