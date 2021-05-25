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
from DISClib.DataStructures import arraylistiterator as it 
from DISClib.DataStructures import mapentry as me

from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mt
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(tipo,alpha,maptyp):
    """
    Inicializa el catálogo de videos. Crea una lista vacia para guardar
    todos los videos, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y videos. Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
               'category': None,
               "videostags": None,
               "country":None,
               "vid": None
               }
    catalog['videos'] = lt.newList(tipo)
    catalog['videostags'] = mp.newMap(200,
                                maptype=maptyp,
                                loadfactor=alpha,
                                comparefunction=compareTagIds)

    
    catalog['category'] = mp.newMap(70,
                                   maptype='PROBING',
                                   loadfactor=0.5)
    catalog['country'] = mp.newMap(70,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareAuthorsByName)
    

    return catalog

# ==============================
# Funciones para crear datos
# ==============================

def newcategory(id, name):
    """
    Esta estructura almancena los tags utilizados para marcar libros.
    """
    tag = {'name': '', 'tag_id': ''}
    tag['name'] = name
    tag['tag_id'] = id
    return tag


# ==============================
# Funciones para agregar informacion al catalogo
# ==============================

def addVideo(catalog, video):
    # Se adiciona el video a la lista de videos
    lt.addLast(catalog['videos'], video)
    moj= mp.contains(catalog["videostags"],video['category_id']) 
    if moj :
        valoactual=mp.get(catalog["videostags"],video["category_id"])
        valor= me.getValue(valoactual)
        lt.addLast(valor,video)
    else:
        valor=lt.newList("ARRAY_LIST")
        mp.put(catalog['videostags'], video['category_id'], valor)
    
    addCountry(catalog,video["country"].strip(),video)
    

    # Se obtiene el autor del video

def addid(catalog, category):
    """
    Adiciona un tag a la lista de tags
    """

    lista = category["id\tname"].split("\t ")

    category["id"] = lista[0]
    category["name"] = lista[1].strip()
    
    mp.put(catalog['category'], category["name"], category["id"])

def addCountry(catalog, country_n,video):
    """
    param catalog: el catálogo de videos subidos con loadData()
    param country_n: nombre del país que se va a guardar 
    param video: c/ video 
    returns: Adicional por país específico
    """
    pays= catalog["country"]
    moj= mp.contains(pays,country_n)
    if moj:
        valoactual = mp.get(pays,country_n) 
        valor = me.getValue(valoactual)
    else:
        mp.put(pays,country_n,lt.newList("ARRAY_LIST"))
        country = mp.get(pays,country_n)
        valor= me.getValue(country)
    lt.addLast(valor,video)

def addvid(catalog,vid_n,video):
    """
    param catalog: el catálogo de videos subidos con loadData()
    param vid_n: nombre del país que se va a guardar 
    param video: c/ video 
    returns: Adicional por país específico
    """
    Video_id = catalog["vid"]
    moj= mp.contains(Video_id,vid_n)
    if moj:
        valoactual = mp.get(Video_id,vid_n) 
        valor = me.getValue(valoactual)
    else:
        mp.put(Video_id,vid_n,lt.newList("ARRAY_LIST"))
        videoId = mp.get(Video_id,vid_n)
        valor= me.getValue(videoId)
    lt.addLast(valor,video)



# ==============================
# Funciones de consulta
# ==============================

#-------------------------------
# REQUERIMIENTO 1
#-------------------------------

def getvideosbytag(catalog, tag, size, pais):
    videospais = lt.newList()
    tagg=mp.get(catalog["category"],tag) 
    taggg=me.getValue(tagg) 
    valor=mp.get(catalog["videostags"],taggg) 

    tema=me.getValue(valor) 
    videos = mt.sort(tema, cmpVideosByViews)
    for cont in range(1,  lt.size(videos)):
        video = lt.getElement(videos, cont)

        if video["country"] == pais:
            lt.addLast(videospais,video)
    videos = lt.subList(videospais,1,size)
    return videos

#-------------------------------
# REQUERIMIENTO 3
#-------------------------------
def gettrendingvidtag(catalog, tag):
    
    tagg=mp.get(catalog["category"],tag) 
    taggg=me.getValue(tagg) 
    valor=mp.get(catalog["videostags"],taggg) 
    tema=me.getValue(valor) 
    videos = mt.sort(tema,cmpfunction= cmpfunctionByVideoid)
    max = 0
    contador=1
    for cont in range(1,  lt.size(videos)):
        
        if (cont+1) < (lt.size(videos)):
            dato1 = lt.getElement(videos, cont)
            dato2 = lt.getElement(videos, cont+1)

            if dato1["video_id"] == dato2["video_id"] and dato1["video_id"] != "#NAME?":

                contador+=1
                if contador > max:
                    max = contador
                    fijo=dato1
            else :
                contador=1
    print("Dias en tendecia : "+str(max))
    return (fijo)
#-------------------------------
# REQUERIMIENTO 2
#-------------------------------
def TrendingVidCountry(catalog,country):
    """
    Si estuviera ordenado REQ 2 
    """
    video_Tct = lt.newList()
    # filtro por país 
    valor=mp.get(catalog["country"],country) 
    tema=me.getValue(valor) 
    videos = mt.sort(tema,cmpfunction= cmpfunctionByVideoid)
    
    value_search = trending_days(videos)
    
    # filtro por video_id 
    for cont in range(1,  lt.size(videos)):
        video = lt.getElement(videos, cont)

        if video["video_id"] == value_search[1]:
            lt.addLast(video_Tct,video)
    flt = lt.subList(video_Tct,1,1)
    print("Dias en tendencia:",value_search[0])
    return flt

def trending_days(videos):
    
    trending_d = 0 
    video_ext = None 
    dicc= {}
    iterador = it.newIterator(videos)
        
    while it.hasNext(iterador):

        pos_actual= it.next(iterador)["video_id"]

        if pos_actual in dicc.keys():
            dicc[pos_actual] +=1
            if  dicc[pos_actual]> trending_d:
                trending_d=  dicc[pos_actual]
                video_ext = pos_actual
        else:
            dicc[pos_actual]= 1
    return (trending_d,video_ext)
#-------------------------------
# REQUERIMIENTO 4
#-------------------------------
def VideoByTagLikes(catalog,pais,size,tag):
    # variables adicionales 
    videosct = lt.newList("ARRAY_LIST")
    # filtro por pais 
    valor=mp.get(catalog["country"],pais) 
    tema=me.getValue(valor) 
    videos = mt.sort(tema,cmpfunction= cmpVideosByLikes)
    # filtro por tag
    iterador = it.newIterator(videos)

    while it.hasNext(iterador):
        tag_c = it.next(iterador) 
        if (tag in str(tag_c["tags"])) == True:
            lt.addLast(videosct, tag_c)
    # Obtención por el size dado por el usuario 
    final_lt = lt.subList(videosct, 1, lt.size(videosct))
    if lt.size(videosct)< size:
        # En caso en el que el size de la lista sea menor al size dado por el usuario
        final_lt = lt.subList(videosct, 1, lt.size(videosct))
    else:
        final_lt = lt.subList(videosct, 1, size)
    return final_lt


# Funciones de Tamaño

def videosSize(catalog):
    """
    Número de libros en el catago
    """
    return lt.size(catalog['videos'])

def categorySize(catalog):
    """
    Número de libros en el catago
    """
    return mp.size(catalog['category'])


# Funciones de ordenamiento


def cmpVideosByLikes(video1, video2):
    return (float(video1['likes']) > float(video2['likes']))


def cmpVideosByViews(video1, video2):
    return (float(video1['views']) > float(video2['views']))


def comparcategory(categ, id):
    id = me.getKey(id)
    print(id)
    return (categ == id)

def cmpfunctionByVideoid(video1, video2):
    
    return ((video1['video_id']) < (video2['video_id']))

def compareAuthorsByName(keyname, author):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(author)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compareTagIds(id, tag):
    tagentry = me.getKey(tag)
    if (int(id) == int(tagentry)):
        return 0
    elif (int(id) > int(tagentry)):
        return 1
    else:
        return 0