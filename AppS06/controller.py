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
import datetime as dt


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Inicialización del Catálogo de vídeos



def initCatalog(factorcarga: int, tipomapa: int):
    """
    Llama la funcion de inicializacion del catalogo del modelo.

    Retorna el catálogo.
    """
    catalog = model.newCatalog(factorcarga, tipomapa)
    return catalog



# Funciones para la carga de datos



def loadData(catalog):
    """
    Args:
        catalog: Catálogo de videos.

    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    loadCategoryID(catalog)
    loadVideos(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory



def loadCategoryID(catalog):
    """
    Args:
        catalog: Catálogo de videos.

    Carga las categorías del archivo.
    """
    categoryfile = cf.data_dir + 'videos/category-id.csv'
    input_file = csv.DictReader(open(categoryfile, encoding='utf-8'), delimiter="\t")
    for category in input_file:
        filtered_category = {
            'id': category['id'],
            'name': (category['name']).replace(" ", '')  # quitar los espacios
        }

        model.addCategoryID(catalog, filtered_category)




def loadVideos(catalog):
    """
    Args:
        catalog: Catálogo de videos.

    Carga todos los vídeos del archivo y los agrega a la lista de vídeos
    """
    videosfile = cf.data_dir + 'videos/videos-large.csv'  # videos-large para la entrega
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in input_file:

        filtered_video = {
            'video_id': video['video_id'],
            'trending_date': dt.datetime.strptime(video['trending_date'], '%y.%d.%m').date(),
            'title': video['title'],
            'channel_title': video['channel_title'],
            'category_id': int(video['category_id']),
            'publish_time': dt.datetime.strptime(video['publish_time'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            'tags': video['tags'],
            'views': int(video['views']),
            'likes': int(video['likes']),
            'dislikes': int(video['dislikes']),
            'country': video['country'],
            'dias_t': 1
        }


        model.addVideo(catalog, filtered_video)
        model.addVideoCountry(catalog, filtered_video['country'], filtered_video)



# Funciones de ordenamiento



def sortVideos(catalog, cmp: int):
    """
    Args:
        catalog: Catálogo de videos.
        cmp: (1) cmpVideosByViews (2) cmpVideosByTitle (3) cmpVideosByID (4) cmpVideosByLikes

    Return:
        list: Ordena los vídeos según sus views.
    """

    return model.sortVideos(catalog, cmp)



# Funciones de consulta sobre el catálogo



def primerVideo(catalog):
    """
    Args:
        catalog: Catálogo de videos.

    Return:
        video1: Retorna el primero video cargado en el catálogo.
    """
    video1 = model.primerVideo(catalog)
    return video1




def getVideosByCountry(catalog, countryName):
    """
    Args:
        catalog: Catálogo de videos.
        countryName: Nombre del país para flitrar los videos.

    Return:
        list: catálogo filtrado por el nombre del país.
    """
    country = model.getVideosByCountry(catalog, countryName)
    return country




def getVideosByCategory(catalog, categoryName, categoryCatalog):
    """
    Args:
        catalog: Catálogo de videos.
        categoryName: Nombre de la categoría para flitrar los videos.

    Return:
        list: catálogo filtrado por el nombre de la categoría.
    """

    category = model.getVideosByCategory(catalog, categoryName, categoryCatalog)

    return category




def getVideosByTag(catalog, tag):
    """
    Args:
        catalog: Catálogo de videos
        tag: Nombre del tag ingresado por el usuario

    Return:
        tag: Catálogo filtrado de acuerdo con el tag ingresado por parámetro
    """
    tag = model.getVideosByTag(catalog, tag)
    return tag



# Funciones de operaciones sobre el catálogo



def masDiasTrending(catalog, llave: int):
    """
    Args:
        catalog: Catálogo ordenado según los Títulos
        llave: (1) 'title' o (2) 'video_id'

    Return:
        video_mayor_dias: Video que ha tenido más días de tendencia.
    """
    catalog = model.masDiasTrending(catalog, llave)
    return catalog




def quitarCopiasLikes(ord_videos, size):
    """
    Args:
        ord_videos: Catálogo de videos ordenado.

    Return:
        ord_videos: Catálogo de videos ordenado y filtrado para que no se repita un mismo video.
    """
    return model.quitarCopiasLikes(ord_videos, size)


# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter() * 1000)


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
    delta_memory = delta_memory / 1024.0
    return delta_memory
