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

def mostrar_elementos(info_elementos: dict, tipo_ele: str):
    """
    PRE: "info_elementos" es un diccionario con los nombres de los elementos como clave y sus 
    respectivos ids como valores.
    
    POST: No devuelve nada solo muestra por panatalla los elementos solicitados.
    """

    cont = 0

    for elemento in info_elementos.keys():
        print (f'{cont}-{elemento}')
        cont += 1
    
    print(f'Se encontraron {cont} {tipo_ele}\n')

def guardar_info_elementos(elementos: dict, info_carpetas:dict, info_archivos):
    """
    PRE: recibe los diccionarios "elementos":
    [{id: 'id_elemento', name: 'nombre del elemento', mimeType: '(el tipo de archivo q sea'}]
    "info_carpetas" [{id: id_carpeta, name:'nombre carpeta}] y
    "info_archivos" [{id: id_archivo, name:'nombre archivo}].
    
    POST: No devuelve nada. Modifica por parametro los diccionario "info_carpetas" e 
    "info_archivos" colocando como clave los nombres de los elementos y sus id's como valores.
    """
    #voy a facilitar la funcion suponiendo q no hay 2 carpetas o archivos con el mismo nomrbe, 
    #asi puedo buscar las carpeta directamente por el nombre q me indica el usuario

    for elemento in elementos:
        if elemento['mimeType'] == 'application/vnd.google-apps.folder':
            info_carpetas[ elemento['name'] ] = elemento['id']        
        else:
            info_archivos[ elemento['name'] ] = elemento['id']


#LISTAR ELEMENTOS EL REMOTO
def listar_elementos(query: str) -> dict:
    """
    PRE: Recibe el string "query" con la consulta a enviar a la API de drive.
    
    POST: Devuelve los diccionarios "info_carpetas" e "info_archivos" con los nombres de los 
    elementos como clave y sus id's como valores.
    """
    page_token = None
    cortar = False

    info_carpetas = dict()
    info_archivos = dict()
    while not cortar:
        #files().list() devuelve un diccionario de diccionarios, q guardo en "resultados"
        resultados = service().files().list(q= query,
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name, mimeType)',
                                            pageToken=page_token).execute()
        #print(resultados)  #testing
        #En el dict resultados, una clave es 'files', que es una lista de diccionarios donde 
        #cada diccionario es un elemento de dicha lista. Lo guardo en elementos.
        
        elementos = resultados['files']

        #print(elementos) #testing
        guardar_info_elementos(elementos, info_carpetas, info_archivos)

        #chequeo si hay mas resultados
        page_token = resultados.get('nextPageToken')
        if page_token is None:
            cortar = True

    return info_carpetas, info_archivos


def armado_de_consulta(id_elemento: str) -> str:
    """
    PRE: "id_elemento" es el id de la carpeta o archivo que selecciono el usurario
    
    POST: devuelve el string "query" con la consulta a buscar en el drive
    """

    print('1-Busqueda manual (lista todas las carpetas y archivos disponibles)\n2-Busqueda personalizada')
    opc = int(validar_opcion(1,2)) 
    if opc == 1:
        query = f" '{id_elemento}' in parents" 
    
    else:
        #print('\nQue desea buscar?\n1-Carpetas\n2-Archivos')
        #opc = int(validar_opcion(1,2))
        palabra = input('ingerse palabra clave COMPLETA: ')  #contains solo busca palabras completas no letras!
        query = f" '{id_elemento}' in parents and fullText contains '{palabra}' " 

        # if opc == 1:
        #     mimeType = 'application/vnd.google-apps.folder'
        #     print('CARPETAS SEGUN LO SOLICITADO\n')
        #     query = f"mimeType = 'application/vnd.google-apps.folder' and fullText contains '{palabra}'"

        # else:
        #     print('ARCHIVOS SEGUN LO SOLICITADO\n')
        #     query = f" mimeType != 'application/vnd.google-apps.folder' and fullText contains '{palabra}'"
        
        print(query) #testing
    
    return query


def seleccionar_elementos(elementos_ids: dict) -> list:
    
    elementos_seleccionados = elementos_ids
    
    return elementos_seleccionados


def consultar_elementos():
    """
    PRE:

    POST: Redirige a otras funciones de filtro y busqueda de archivos.
    """
    
    print('BUSCADOR DE DRIVE')
    cortar = False
    id_elemento = 'root'
    while not cortar:

        query = armado_de_consulta(id_elemento)
        info_carpetas, info_archivos = listar_elementos(query)
        
        print('Seleccione el archivo o carpeta q desea abrir')
        id_elemento = input('')
        
        #aca posiblemente mande a una funcion para traer el id del diccionario

        
        print('CARPETAS')
        mostrar_elementos(info_carpetas, 'carpetas')

        print('ARCHIVOS')
        mostrar_elementos(info_archivos,'archivos')

        #elementos_seleccionados = seleccionar_elementos(elementos_ids)
        
        #print (elementos_seleccionados)
        
        #return elementos_seleccionados

consultar_elementos()

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
    
    carpeta_id = consultar_elementos()
    # carpeta_id = '1_qDcJ2I4xpNgrvYyqXtWv1w0ELP0N27m'
    
    # file_metadata = {
    #                 'name': 'prueba_upload.txt',
    #                 'parents': [carpeta_id]
    #             }
 
    # media = MediaFileUpload(ruta_archivo)

    # file = service().files().create(body = file_metadata,
    #                                     media_body = media,
    #                                     fields = 'id').execute()
    
    # print ('File ID: %s' % file.get('id'))

#subir_archivos()

    #print('file name %:' % file.get('name'))

    # #print('ok')
