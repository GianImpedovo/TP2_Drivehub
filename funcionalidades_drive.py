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

def mostrar_elementos(elementos):
    resultados_tot = 0
    for elemento in elementos:
        print (elemento['name'])
        resultados_tot += 1


def guardar_ids_de_elementos(elementos_ids: dict, elementos:dict):
    """
    PRE: recibe los diccionarios "elementos_ids" {nombre de los elemento: id del elemento}
    y "elementos" [{id: id_elemento, name:''nombre del elemento}]
    
    POST: No devuelve nada. Modifica por parametro el diccionario "elementos_ids" colocando
    como clave los nombres de los elementos y sus id's como valores
    """
    #voy a facilitar la funcion suponiendo q no hay 2 carpetas o archivos con el mismo nomrbe, 
    #asi puedo buscar las carpeta directamente por el nombre q me indica el usuario

    for elemento in elementos:
        
        elementos_ids[ elemento['name'] ] = elemento['id']        
        #file_ids[ carpeta['id'] ] = carpeta['name']


#LISTAR ELEMENTOS EL REMOTO
def listar_elementos(query: str) -> dict:
    """
    PRE: Recibe el string "query" con la consulta a enviar a la API de drive
    
    POST: Lista los elementos pedidos (carpetas o archivos) y devuelve el diccionario "elementos_ids" con los 
    nombres de los elementos como clave y sus id's como valores
    """
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
        #print(elementos)
        guardar_ids_de_elementos(elementos_ids, elementos)

        #chequeo si hay mas resultados
        page_token = resultados.get('nextPageToken', None)
        if page_token is None:
            cortar = True
    
    #print(f'\nSe encontraron {resultados_tot} elementos')
    
    return elementos_ids


def armado_de_sentencia_consulta() -> str:
    """
    PRE:
    
    POST: devuelve el string "query" con la consulta a bucar en drive
    """
    print('BUSCADOR DE DRIVE')
    print('1-Busqueda manual (lista todas las carpetas disponibles)\n2-Busqueda personalizada')
    opc = int(validar_opcion(1,2))
    if opc == 1:
        print('CARPETAS DISPONIBLES EN DRIVE\n')
        query ="mimeType= 'application/vnd.google-apps.folder'" #para buscar carpetas
    else:
        print('\nQue desea buscar?\n1-Carpetas\n2-Archivos')
        opc = int(validar_opcion(1,2))

        palabra = input('ingerse palabra clave de busqueda: ')  #contains solo busca palabras completas no letras!
        if opc == 1:
            print('CARPETAS SEGUN LO SOLICITADO\n')
            query = f"mimeType = 'application/vnd.google-apps.folder' and fullText contains '{palabra}'"

        else:
            print('ARCHIVOS SEGUN LO SOLICITADO\n')
            query = f" mimeType != 'application/vnd.google-apps.folder' and fullText contains '{palabra}'"
        
        print(query) #testing
    
    return query


def seleccionar_elementos(elementos_ids: dict) -> :
    mostar_elementos()


def consultar_elementos():
    """
    PRE:

    POST: Redirige a otras funciones de filtro y busqueda de archivos  y devuelve el diccionario
    "elementos_ids" con los nombres de los archivos y sus ids como valores
    """
    print('CONSULTAR ARCHIVOS DE DRIVE\n')
    
    query= armado_de_sentencia_consulta()
    
    elementos_ids = listar_elementos(query)
    
    seleccionar_elementos(elementos_ids)

    return elementos_ids


def descargar_archivos():
    """
    PRE:
    POST: No devuelve nada. Permite descargar el archivo seleccionado en drive por el usuario. 
    """
    elementos_ids = consultar_elementos()
    #print(elementos_ids)

    #print(file_ids)
    pass

def seleccionar_archivo_subida():
    print('Seleccione el archivo o carpeta de su computadora que desea subir')
    pass


def subir_archivos():
    
    ruta_archivo = seleccionar_archivo_subida()
    ruta_archivo = 'prueba_upload_1.txt'
    
    carpeta_id = seleccionar_elemento()
    carpeta_id = '1_qDcJ2I4xpNgrvYyqXtWv1w0ELP0N27m'
    
    file_metadata = {
                    'name': 'prueba_upload.txt',
                    'parents': [carpeta_id]
                }
 
    media = MediaFileUpload(ruta_archivo)

    file = service().files().create(body = file_metadata,
                                        media_body = media,
                                        fields = 'id').execute()
    
    print ('File ID: %s' % file.get('id'))

subir_archivos()

    #print('file name %:' % file.get('name'))

    # #print('ok')
