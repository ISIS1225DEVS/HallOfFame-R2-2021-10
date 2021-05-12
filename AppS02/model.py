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
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.DataStructures import mapentry as me
import time
assert cf

"""
Se define la estructura de un catálogo de videos.
El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construcción de modelos


def newCatalog():
    """ Inicializa el catálogo de videos

    Crea dos listas vacia para guardar todos los videos
    y las categorías

    Se crean indices (Maps) por los siguientes criterios:
    Categoría
    País

    Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
               'category_id': None,
               'category': None,
               'country': None}

    """
    Esta lista contiene todo los videos encontrados
    en los archivos de carga.  Estos videos no estan
    ordenados por ningun criterio.  Son referenciados
    por los indices creados a continuacion.
    """
    catalog['videos'] = lt.newList('ARRAY_LIST')

    """
    Esta lista contiene las categorías
    """
    catalog['category_id'] = lt.newList('ARRAY_LIST')

    """
    A continuación se crean indices por diferentes criterios
    para llegar a la informacion consultada.  Estos indices no
    replican informacion, solo referencian los videos de la lista
    creada en el paso anterior.
    """

    """
    Este indice crea un map cuya llave es la categoría del video
    """
    catalog['category'] = mp.newMap(
        40,
        maptype='PROBING',
        loadfactor=0.5)

    """
    Este indice crea un map cuya llave es el país del video
    """
    catalog['country'] = mp.newMap(
        20,
        maptype='PROBING',
        loadfactor=0.5)

    return catalog


# Funciones para agregar información al catalogo


def addVideo(catalog, video):
    """
    La función de addVideo() adiciona los videos a una lista de videos,
    a su vez los adiciona a los mapas de 'category' y de 'country'
    """
    lt.addLast(catalog['videos'], video)
    addVideoOnMap(catalog, video['category_id'], video, 'category')
    addVideoOnMap(catalog, video['country'], video, 'country')


def addCategory(catalog, category):
    """
    La función de addCategory() adiciona una categoría a la
    lista de categorías
    """
    c = newSeparator(category, 'category')
    lt.addLast(catalog['category_id'], c)


def addVideoOnMap(catalog, int_input, video, catalog_key):
    """
    La función de addVideoOnMap() adiciona el video al mapa
    que se ha seleccionado.
    Args:
        catalog: Catalogo de videos
        int_input: Llave a analizar
        video: Video a añadir
        catalog_key: Especifica cuál catalogo
    """
    selected_map = catalog[catalog_key]
    existkey = mp.contains(selected_map, int_input)
    if existkey:
        entry = mp.get(selected_map, int_input)
        value = me.getValue(entry)
    else:
        value = newSeparator(int_input, catalog_key)
        mp.put(selected_map, int_input, value)
    lt.addLast(value['videos'], video)


def newSeparator(key, classifier):
    """
    La función de newSeparator() crea una nueva estructura
    para modelar los mapas.
    Args:
        key: Llave del mapa
        classifier: Especifica cuál mapa
    """
    if classifier == 'country':
        separator = {"country_name": "", "videos": None}
        separator['country_name'] = key
        separator['videos'] = lt.newList('ARRAY_LIST', None)
    elif classifier == 'category':
        separator = {"c_id": "", "videos": None}
        separator['c_id'] = key
        separator['videos'] = lt.newList('ARRAY_LIST', None)
    return separator


# Funciones de consulta


def getVideosByCriteriaList(catalog, criteria, x):
    """
    La función de getVideosByCriteriaList() filtra los videos por un
    criterio específico dado un x. El catálogo debe ser una lista.
    """
    listaretorno = lt.newList("ARRAY_LIST")
    for element in lt.iterator(catalog):
        nombre_pais = element.get(criteria)
        if nombre_pais == x:
            lt.addLast(listaretorno, element)

    return listaretorno


def getVideosByCriteriaMap(catalog, criteria, key):
    """
    La función de getVideosByCriteriaMap() filtra los videos por un
    criterio específico dado un key. El catálogo debe ser un mapa.
    """
    values = catalog[criteria]
    entry = mp.get(values, str(key))
    result = me.getValue(entry)
    return result


def getVideosByCategoryAndCountry(catalog, category, country):
    """
    La función de getVideosByCriteriaMap() filtra los videos por una
    llave y categoría específicas.
    """
    sublist = getVideosByCriteriaMap(
        catalog, 'category', category).get('videos')
    sublist2 = getVideosByCriteriaList(sublist, 'country', country)
    return sortVideos(sublist2, lt.size(sublist2), 'cmpVideosByViews')


def getMostTrendingDaysByID(videos):
    """
    La función de  getMostTrendingDaysByID() itera la lista ordenada y
    retorna el elemento que más se repite.
    """
    elemento = lt.firstElement(videos)
    mayor_titulo = None
    mayor = 0
    i = 0

    for video in lt.iterator(videos):
        if video['video_id'] == elemento['video_id']:
            i += 1
        else:
            if i > mayor:
                mayor_titulo = elemento
                mayor = i
            i = 1
            elemento = video

    if i > mayor:
        mayor_titulo = elemento
        mayor = i
    return (mayor_titulo, mayor)


def getVideosByCountryAndTag(catalog, tag, country):
    """
    La función de getVideosByCountryAndTag() filtra los videos por un país
    y tag específico
    """
    sublist = getVideosByCriteriaMap(catalog, 'country', country).get('videos')
    sublist2 = getVideosByTag(sublist, tag)
    sorted_list = sortVideos(
        sublist2, int(lt.size(sublist2)), 'comparelikes')
    return sorted_list


def getVideosByTag(videos, tag):
    """
    La función de getVideosByTag() filtra los videos por un tag
    específico
    """
    lista = lt.newList('ARRAY_LIST')
    i = 1

    while i <= lt.size(videos):
        c_tags = lt.getElement(videos, i).get('tags')
        tagpresence = tag in c_tags

        if tagpresence:
            element = lt.getElement(videos, i)
            lt.addLast(lista, element)

        i += 1

    return lista


def videosSize(catalog):
    """
    Número de videos en el catalogo
    """
    return lt.size(catalog['videos'])


def categoriesSize(catalog):
    """
    Numero de categorias en el catalogo
    """
    return mp.size(catalog['category'])


def countriesSize(catalog):
    """
    Numero de paises en el catalogo
    """
    return mp.size(catalog['country'])


# Funciones utilizadas para comparar elementos dentro de una lista


def cmpVideosByViews(video1, video2) -> bool:
    """
    La función de cmpVideosbyViews() retorna True or False si las visitas
    de un video son mayores o menores a las visitas de otro video
    """
    return (float(video1['views']) > float(video2['views']))


def comparelikes(video1, video2):
    """
    La función de comparelikes() retorna True or False si dados los likes
    de un video, este es mayor o menor a los likes de otro video
    """
    return (float(video1['likes'])) > (float(video2['likes']))


def comparetitles(video1, video2):
    """
    La función de comparetitles() retorna True or False si el título de un
    video es mayor al de otro video ordenando alfabéticamente
    """
    return (video1['title']) > (video2['title'])


# Funciones de ordenamiento


def sortVideos(catalog, size, cmp):
    """
    La Función sortVideos() organiza los videos de acuerdo
    al parámetro cmp.
    """
    sub_list = lt.subList(catalog, 0, size)
    sub_list = sub_list.copy()
    start_time = time.process_time()

    if cmp == 'cmpVideosByViews':
        sorted_list = ms.sort(sub_list, cmpVideosByViews)
    if cmp == 'comparetitles':
        sorted_list = ms.sort(sub_list, comparetitles)
    if cmp == 'comparelikes':
        sorted_list = ms.sort(sub_list, comparelikes)

    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list


# Funciones que no se utilizan

'''
def getMostTrendingDaysByIDv1(videos):
    ids = mp.newMap(
        500,
        maptype='PROBING',
        loadfactor=0.8)
    pos = mp.newMap(
        500,
        maptype='PROBING',
        loadfactor=0.8)
    ids_list = lt.newList('ARRAY_LIST')

    i = 1

    while i <= lt.size(videos):
        video_id = lt.getElement(videos, i).get('video_id')
        presence = lt.isPresent(ids_list, video_id) != 0

        if presence:
            n = int(mp.get(ids, video_id).get('value'))
            n += 1
            mp.put(ids, video_id, n)
        else:
            mp.put(ids, video_id, 1)
            mp.put(pos, video_id, i)
            lt.addLast(ids_list, video_id)
        i += 1

    mayor = video_id
    repeticiones_mayor = int(mp.get(ids, mayor).get('value'))
    mayor = video_id
    repeticiones_mayor = int(mp.get(ids, mayor).get('value'))

    for each_id in ids_list:
        repetitions = int(mp.get(ids, each_id).get('value'))
        if repetitions > repeticiones_mayor:
            mayor = each_id
            repeticiones_mayor = repetitions

    position = mp.get(pos, mayor).get('value')
    repetitions = mp.get(ids, mayor).get('value')
    result = lt.getElement(videos, position)

    return (result, repetitions)
'''
