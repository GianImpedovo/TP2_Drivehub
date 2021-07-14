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

def guardar_ids_de_carpetas(file_ids: dict, carpetas:dict):
    
    #voy a facilitar la funcion suponiendo q no hay 2 carpetas con el mismo nomrbe, 
    #asi puedo buscar las carpeta directamente por el nombre q me indica el usuario

    for carpeta in carpetas:
        
        file_ids[ carpeta['name'] ] = carpeta['id']        
        #file_ids[ carpeta['id'] ] = carpeta['name']


#LISTAR TODAS LAS CARPETAS EN EL REMOTO
def listar_todas_carpetas() -> None:
    """
    PRE: 
    POST: Muestra por pantalla todas las carpetas disponibles en drive y devuelve un 
    diccionario con todos los nombres de las carpetas y sus respectivos 'ids'
    """
    print('CARPETAS DISPONIBLES EN EL REMOTO\n')
    page_token = None
    cortar = False
    resultados_tot = 0
    file_ids = dict()
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
        guardar_ids_de_carpetas(file_ids, carpetas)
        
        for carpeta in carpetas:
            print (carpeta['name'])
            resultados_tot += 1

        #chequeo si hay mas resultados
        page_token = resultados.get('nextPageToken', None)
        if page_token is None:
            cortar = True
    
    print(f'\nResultados totales: {resultados_tot}')
    
    return file_ids

file_ids = listar_todas_carpetas()

def busqueda_personalizada():
    """
    PRE: 
    POST: 
    """
    print('BUSCADOR DE ARCHIVOS DE DRIVE\n')
    query = input= ('')
    page_token = None
    cortar = False
    resultados_tot = 0
    file_ids = dict()
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
        guardar_ids_de_carpetas(file_ids, carpetas)
        
        for carpeta in carpetas:
            print (carpeta['name'])
            resultados_tot += 1

        #chequeo si hay mas resultados
        page_token = resultados.get('nextPageToken', None)
        if page_token is None:
            cortar = True
    
    print(f'\nResultados totales: {resultados_tot}')
    
    return file_ids

'''
def consultar_archivos():
    print('CONSULTAR ARCHIVOS DE DRIVE\n')
    print('1- Listar carpetas disponibles\n 2-Busqueda personalizada\n')
    opc = validar_opcion(1,2)
    if opc == 1:
        listar_todas_carpetas()
    elif:
        busqueda_personalizada()

'''
        



#print(file_ids)


# file_metadata = {'name': 'prueba_1.txt'}
# media = MediaFileUpload('C:/Users/German/Documents/archivos german/Algortimos y Programacion I 95.14/Tp-drive-Hub/testing/prueba_0_api/apuntes_tp2.txt', mimetype= 'text/plain')

# file = service().files().create(body=file_metadata,
#                                     media_body=media,
#                                     fields='id').execute()
# print ('File ID: %s' % file.get('id'))
# #print('file name %:' % file.get('name'))

# #print('ok')
