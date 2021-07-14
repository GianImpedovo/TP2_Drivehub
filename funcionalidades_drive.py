from service_drive import obtener_servicio as service
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os


def validar_opcion(opc_minimas: int, opc_maximas: int, texto: str = '') -> str:
    """
    PRE: "opc_minimas" y "opc_maximas" son dos números enteros que 
    simbolizan la cantidad de opciones posibles.

    POST: Devuelve en formato string la var "opc" con un número 
    entero dentro del rango de opciones.
    """
    opc = input("{}".format(texto))
    while not opc.isnumeric() or int(opc) > opc_maximas or int(opc) < opc_minimas:
        opc = input("Por favor, ingrese una opcion valida: ")
    
    return opc

def guardar_ids_de_elementos(elementos_ids: dict, elementos:dict):
    
    #voy a facilitar la funcion suponiendo q no hay 2 carpetas o archivos con el mismo nomrbe, 
    #asi puedo buscar las carpeta directamente por el nombre q me indica el usuario

    for elemento in elementos:
        
        elementos_ids[ elemento['name'] ] = elemento['id']        
        #file_ids[ carpeta['id'] ] = carpeta['name']

#LISTAR TODAS LAS CARPETAS EN EL REMOTO

def listar_todas_carpetas() -> None:
    """
    PRE: 
    POST: Muestra por pantalla todas las carpetas disponibles en drive y devuelve un 
    diccionario con todos los nombres de las carpetas y sus respectivos 'ids'
    """
    
    page_token = None
    cortar = False
    resultados_tot = 0
    elementos_ids = dict() #elementos pueden ser carpetas o archivos
    while not cortar:
        #traigo resultados
        #ACLARACIONES IMPORTANTES QUIZA OBVIAS PERO ME COSTARON:
        #.list() DEVUELVE UN DICCIONARIO DE DICCIONARIOS, DONDE UNA DE LAS CLAVES ES files(), 
        #q a su vez es un diccionario.
        resultados = service().files().list(q="mimeType= 'application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()
        #print(resultados)
        #en el dict files, accedo a la clave 'name'

        carpetas = resultados['files']
        guardar_ids_de_elementos(elementos_ids, carpetas)
        
        for carpeta in carpetas:
            print (carpeta['name'])
            resultados_tot += 1

        #chequeo si hay mas resultados
        page_token = resultados.get('nextPageToken', None)
        if page_token is None:
            cortar = True
    
    print(f'\nResultados totales: {resultados_tot}')
    
    return folder_ids

#file_ids = listar_todas_carpetas()
# print(file_ids)


def listar_elementos(query):
    """
    PRE: 
    POST: 
    """
    print('BUSCADOR DE ARCHIVOS DE DRIVE\n')
    #searchFile(5,"name contains 'prueba' and fullText contains 'prueba' and mimeType = 'text/plain'")
    #searchFile(3,"name contains 'prueba' and mimeType = 'text/plain' ")
    # palabra = input ('ingerse palabra de busqueda clave: ')
    # query = f"name contains '{palabra}'"

    page_token = None
    cortar = False
    resultados_tot = 0
    elementos_ids = dict()
    while not cortar:
        #traigo resultados
        #ACLARACIONES IMPORTANTES QUIZA OBVIAS PERO ME COSTARON:
        #.list() DEVUELVE UN DICCIONARIO DE DICCIONARIOS, DONDE UNA DE LAS CLAVES ES files(), 
        #q a su vez es un diccionario.
        resultados = service().files().list(q= query,
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()
        #print(resultados)
        #en el dict files, accedo a la clave 'name'

        elementos = resultados['files']
        guardar_ids_de_elementos(elementos_ids, elementos)
        
        for elemento in elementos:
            print (elemento['name'])
            resultados_tot += 1

        #chequeo si hay mas resultados
        page_token = resultados.get('nextPageToken', None)
        if page_token is None:
            cortar = True
    
    print(f'\nResultados totales: {resultados_tot}')
    
    return elementos_ids


def armado_de_sentencia_consulta() -> str:
    """
    PRE:
    POST: devuelve el string 'query' con la consulta a bucar en drive
    """
    print('1-Busqueda manual (lista carpetas disponibles)\n2-Busqueda personalizada')
    opc = int(validar_opcion(1,2))
    if opc == 1:
        query ="mimeType= 'application/vnd.google-apps.folder'" #para buscar carpetas
    else:
        print('Que desea buscar?\n 1-Carpetas\n2-Archivos')
        opc = int(validar_opcion(1,2))
        if opc == 1:
            palabra = input ('ingerse palabra clave de busqueda: ')
            query = f"name contains '{palabra}' and mimeType = 'application/vnd.google-apps.folder'"
        # else:
        #     query = 
    
    return query

def consultar_archivos():
    print('CONSULTAR ARCHIVOS DE DRIVE\n')
    
    query= armado_de_sentencia_consulta()
    #print('CARPETAS DISPONIBLES EN EL REMOTO\n')
    
    elementos_ids = listar_elementos(query)
    print(elementos_ids)
    
    #file_ids = busqueda_personalizada()
    #print(file_ids)
        
consultar_archivos()

#print(file_ids)


# file_metadata = {'name': 'prueba_1.txt'}
# media = MediaFileUpload('C:/Users/German/Documents/archivos german/Algortimos y Programacion I 95.14/Tp-drive-Hub/testing/prueba_0_api/apuntes_tp2.txt', mimetype= 'text/plain')

# file = service().files().create(body=file_metadata,
#                                     media_body=media,
#                                     fields='id').execute()
# print ('File ID: %s' % file.get('id'))
# #print('file name %:' % file.get('name'))

# #print('ok')
