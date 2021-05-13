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


import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Sorting import quicksort as quick
from DISClib.DataStructures import listiterator as it
assert cf
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
import tracemalloc




# ========================
# Construccion de modelos
# ========================



def newCatalog():

    catalog = {'videos' : None,  
              'categories' : None,
              'categories_sorted' : None,
              'countries_sorted' : None,
              'country_category_sorted' : None}

    catalog["videos"] = lt.newList("ARRAY_LIST", cmpfunction=comparevideos)
    
    catalog["categories"] = mp.newMap(32, maptype = "PROBING", loadfactor = 0.5, comparefunction=comparecategories)

    catalog["categories_sorted"] = mp.newMap(32, maptype = "PROBING", loadfactor = 0.5, comparefunction=comparecategories)

    catalog["countries_sorted"] = mp.newMap(10, maptype = "PROBING", loadfactor = 0.5, comparefunction=comparecountries)

    catalog["country_category_sorted"] = mp.newMap(320, maptype = "PROBING", loadfactor = 0.5, comparefunction=comparecountries)

    return catalog 



# =============================================
# Funciones para agregar informacion al catalogo
# =============================================



def addVideo(catalog, videoname):

    lt.addLast(catalog["videos"], videoname)

    
def addCategory(catalog, category):

    c = newCategory(category["name"].lstrip(" "), category["id"])
    mp.put(catalog["categories"], category["id"], c)


def addCategorySorted (catalog, videoname):

    category_id = videoname["category_id"]
    category = (mp.get(catalog["categories"], category_id))["value"]["category_name"]

    if mp.contains(catalog["categories_sorted"], category):

        list_exists = mp.get(catalog["categories_sorted"], category)["value"]
        lt.addLast(list_exists, videoname)
        mp.put(catalog["categories_sorted"], category, list_exists)

    else:
        mp.put(catalog["categories_sorted"], category, lt.newList("ARRAY_LIST"))
        new_list = mp.get(catalog["categories_sorted"], category)["value"]
        lt.addLast(new_list, videoname)


def addCountriesSorted (catalog, videoname):

    country = videoname["country"]

    if mp.contains(catalog["countries_sorted"], country):

        list_exists = mp.get(catalog["countries_sorted"], country)["value"]
        lt.addLast(list_exists, videoname)
        mp.put(catalog["countries_sorted"], country, list_exists)

    else:
        mp.put(catalog["countries_sorted"], country, lt.newList("ARRAY_LIST"))
        new_list = mp.get(catalog["countries_sorted"], country)["value"]
        lt.addLast(new_list, videoname)


def addCountryCategorySorted (catalog, videoname):

    category_id = videoname["category_id"]
    category = (mp.get(catalog["categories"], category_id))["value"]["category_name"]

    country = videoname["country"]

    if mp.contains(catalog["country_category_sorted"], country + "/" + category):
        list_exists = mp.get(catalog["country_category_sorted"], country + "/" + category)["value"]
        lt.addLast(list_exists, videoname)
        mp.put(catalog["country_category_sorted"], country + "/" + category, list_exists)

    else:
        mp.put(catalog["country_category_sorted"], country + "/" + category, lt.newList("ARRAY_LIST"))
        new_list = mp.get(catalog["country_category_sorted"], country + "/" + category)["value"]
        lt.addLast(new_list, videoname)



# =================================
# Funciones para creacion de datos
# =================================



def newCategory(name, id):

    category = {"category_name": "", "category_id": ""}
    category["category_name"] = name
    category["category_id"] = id
    return category

    

# ======================
# Funciones de consulta
# ======================



def firstVideo (catalog):

    lista = catalog["videos"]
    primer_video = lt.firstElement(lista)
    title = primer_video["title"]
    channel = primer_video["channel_title"]
    trending_date = primer_video["trending_date"]
    country = primer_video["country"]
    views = primer_video["views"]
    likes = primer_video["likes"]
    dislikes = primer_video["dislikes"]

    video = {"title": title, "channel_title": channel, "trending_date": trending_date, "country": country, "views": views, "likes": likes, "dislikes": dislikes}

    return video


def sortVideosByViews (catalog, category, country):

    tracemalloc.start()
    
    delta_time = -1.0
    delta_memory = -1.0

    start_time = getTime()
    start_memory = getMemory()

    sorted_list_country_category = mp.get(catalog["country_category_sorted"], country + "/" + category)["value"]

    sorted_list = merge.sort(sorted_list_country_category, compVideoByViews)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return delta_time, delta_memory, sorted_list


def sortVideosCountryTrending (catalog, country):

    tracemalloc.start()
    
    delta_time = -1.0
    delta_memory = -1.0

    start_time = getTime()
    start_memory = getMemory()

    sublistcountries = mp.get(catalog["countries_sorted"], country)["value"]

    sorted_list_titles = merge.sort(sublistcountries, compVideoByTitle)

    video_id = ""
    days = 0
    days_max = 0
    video_id_max = "" 
    channel = ""
    channel_max = ""
    title = ""
    title_max = ""

    iterator2 = it.newIterator(sorted_list_titles)
    while it.hasNext(iterator2):
        element = it.next(iterator2)
        idNumber = element["video_id"]

        if video_id != "#NAME":
            if video_id == idNumber:
                days += 1
            
            else:
                if days > days_max:
                    days_max = days
                    video_id_max = video_id
                    channel_max = channel
                    title_max = title
                video_id = element["video_id"]
                channel = element["channel_title"]
                title = element["title"]
                days = 1

    result = ("Titulo: " + str(title_max) + ", Nombre del canal: " + str(channel_max) + 
    ", País: " + str(country) + ", Días: " + str(days_max) )


    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory, result
    

def sortVideosCategoryTrending (catalog, category):

    tracemalloc.start()
    
    delta_time = -1.0
    delta_memory = -1.0

    start_time = getTime()
    start_memory = getMemory()

    sublistcategories = mp.get(catalog["categories_sorted"], category)["value"]

    sorted_list = merge.sort(sublistcategories,compVideoByTitle)

    video_id = ""
    days = 0
    days_max = 0
    video_id_max = "" 
    channel = ""
    channel_max = ""
    title = ""
    title_max = ""
    category_id = None

    iterator3 = it.newIterator(sorted_list)
    while it.hasNext(iterator3):
        element = it.next(iterator3)
        idNumber = element["video_id"]

        if video_id == idNumber:
            days += 1
            
        else:
            if days > days_max:
                days_max = days
                video_id_max = video_id
                channel_max = channel
                title_max = title
                category_id = element["category_id"]
            video_id = element["video_id"]
            channel = element["channel_title"]
            title = element["title"]
            days = 1

    result = ("Titulo: " + str(title_max) + ", Nombre del canal: " + str(channel_max) + 
    ", Id de la categoria: " + str(category_id) + ", Días: " + str(days_max) )

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory, result


def sortVideosLikesTag(catalog, tag, country):

    tracemalloc.start()
    
    delta_time = -1.0
    delta_memory = -1.0

    start_time = getTime()
    start_memory = getMemory()

    sublistcountries = mp.get(catalog["countries_sorted"], country)["value"]

    sublist_tags = lt.newList("ARRAY_LIST")

    iterator1 = it.newIterator(sublistcountries)
    while it.hasNext(iterator1):
        element = it.next(iterator1)
        if str(tag.lower()) in str(element["tags"].lower()):
            lt.addLast(sublist_tags, element)


    sorted_list_likes = merge.sort(sublist_tags, compVideoByLikes)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory, sorted_list_likes



# ================================================================
# Funciones utilizadas para comparar elementos dentro de una lista
# ================================================================



def comparevideos(videotitle1, video):

    if (videotitle1.lower() in video["title"].lower()):
        return -1
    else:
        return 0


def comparecategories(name, category):

    categoryKey = me.getKey(category)

    if (name==categoryKey):
        return 0
    elif (name<categoryKey):
        return -1
    else:
        return 1


def comparecountries (name, country):

    countryKey = me.getKey(country)

    if (name==countryKey):
        return 0
    elif (name<countryKey):
        return -1
    else:
        return 1


def compVideoByViews(video1, video2):

    return (float(video1['views']) > float(video2['views']))


def compVideoByTitle (video1, video2):

    return (str(video1['title']) < str(video2['title']))
    

def compVideoByLikes(video1, video2):

    return (float(video1['likes']) > float(video2['likes']))



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

   

