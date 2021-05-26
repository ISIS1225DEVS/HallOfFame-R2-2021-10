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
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """ Inicializa el catálogo de videos

    Crea una lista vacia para guardar todos los videos

    Se crean indices (Maps) por los siguientes criterios:
    ID videos
    Categoría
    Pais
    Tag

    Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
               'videoIds': None,
               'categories': None,
               'categoriesIds': None,
               'countries': None,
               'tags': None}

    """
    Esta lista contiene todo los videos encontrados
    en los archivos de carga.  Estos videos no estan
    ordenados por ningun criterio.  Son referenciados
    por los indices creados a continuacion.
    """
    catalog['videos'] = lt.newList('SINGLE_LINKED', compareVideoIds)

    """
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada.  Estos indices no
    replican informacion, solo referencian los libros de la lista
    creada en el paso anterior.
    """

    """
    Este indice crea un map cuya llave es el identificador del video
    """
    catalog['videoIds'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareMapVideoIds)

    """
    Este indice crea un map cuya llave es el país del video
    """
    catalog['countries'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareCountriesByName)
    """
    Este indice crea un map cuya llave es la categoría 
    """
    catalog['categories'] = mp.newMap(34500,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=compareCategoryNames)
    """
    Este indice crea un map cuya llave es el Id de la categoría
    """
    catalog['categoriesIds'] = mp.newMap(34500,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareCategoryIds)

    """
    Este indice crea un map cuya llave es el tag del video
    """
    catalog['tags'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareTagsByName)
    
    return catalog

def newVideoCategory(name, id):
    """
    Esta estructura crea una relación entre un tag y los libros que han sido
    marcados con dicho tag.  Se guarga el total de libros y una lista con
    dichos libros.
    """
    category = {'name': '',
           'category_id': '',
           'videos': None}
    category['name'] = name
    category['category_id'] = id
    category['videos'] = lt.newList()
    return category


# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    """
    Esta funcion adiciona un video a la lista de videos,
    adicionalmente lo guarda en un Map usando como llave su Id.
    Adicionalmente se guarda en el indice de paises, una referencia
    al libro.
    """
    lt.addLast(catalog['videos'], video)
    mp.put(catalog['videoIds'], video['video_id'], video)
    country = video['country'] #Se obtiene el país

    category_id = video['category_id'] #Se obtiene el id de la categoria

    entry = mp.get(catalog["categoriesIds"], category_id)
    category_name = me.getValue(entry)

    addVideoCountry(catalog, country.strip(), video)
    addVideoCategory(catalog, category_name, video)
    

def addVideoCountry(catalog, country, video):
    """
    Esta función adiciona un video a la lista de videos de un mismo país.
    """
    countries = catalog['countries']
    existcountry = mp.contains(countries, country)
    if existcountry:
        entry = mp.get(countries, country)
        data = me.getValue(entry)
    else:
        data = newCountry(country)
        mp.put(countries, country, data)
    lt.addLast(data['videos'], video)

def addVideoCategory(catalog, category_name, video):
    """
    Esta función adiciona un video a la lista de videos de una misma categoría.
    """
    categories = catalog['categories']
    existcategory = mp.contains(categories, category_name)
    if existcategory:
        entry = mp.get(categories, category_name)
        data = me.getValue(entry)
    else:
        data = newCategory(category_name)
        mp.put(categories, category_name, data)
    lt.addLast(data['videos'], video)


def addCategory(catalog, category):
    """
    Adiciona un tag a la tabla de tags dentro del catalogo y se
    actualiza el indice de identificadores del tag.
    """
    newcat = newVideoCategory(category['name'], category['id'])
    mp.put(catalog['categories'], category['name'], newcat)
    mp.put(catalog['categoriesIds'], category['id'], category['name'])
   
# Funciones para creacion de datos
def newCountry(name):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    country = {'name': "",
              "videos": None}
    country['name'] = name
    country['videos'] = lt.newList('SINGLE_LINKED', compareCountriesByName)
    return country

def newCategory(name):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    category = {'name': "",
              "videos": None}
    category['name'] = name
    category['videos'] = lt.newList('SINGLE_LINKED', compareCategoriesByName)
    return category


# Funciones de consulta

def videosSize(catalog):
    """
    Número de videos en el catago
    """
    return lt.size(catalog['videos'])


def countriesSize(catalog):
    """
    Numero de paises en el catalogo
    """
    return mp.size(catalog['countries'])


def categoriesSize(catalog):
    """
    Numero de categorías en el catalogo
    """
    return mp.size(catalog['categories'])



# Funciones utilizadas para comparar elementos dentro de una lista

def compareVideoIds(id1, id2):
    """
    Compara dos ids de dos videos
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareMapVideoIds(id, entry):
    """
    Compara dos ids de videos, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

def compareCountriesByName(keyname, country):
    """
    Compara dos nombres de país. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(country)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compareCategoriesByName(keyname, category_name):
    """
    Compara dos nombres de categoria. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(category_name)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1


def compareCategoryNames(name, category):
    catentry = me.getKey(category)
    if (name == catentry):
        return 0
    elif (name > catentry):
        return 1
    else:
        return -1


def compareCategoryIds(id, category):
    catentry = me.getKey(category)
    if (int(id) == int(catentry)):
        return 0
    elif (int(id) > int(catentry)):
        return 1
    else:
        return 0

def compareTagsByName(keyname, tag):
    """
    Compara dos tags de país. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(tag)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

# Funciones de ordenamiento
