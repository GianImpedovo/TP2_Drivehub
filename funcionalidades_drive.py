from typing import Text
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


def retroceder(paths: dict):
    """
    PRE:

    POST:
    """
    for carpeta in paths.keys():
        print(carpeta)

    carpeta = input('Seleccione la carpeta a la que desea retroceder: ')
    
    while carpeta not in paths.keys():
        carpeta = input('Por favor elija una carpeta de las listadas: ')

    id_carpeta = paths[carpeta]

    return id_carpeta, carpeta


def seleccionar_elementos(info_elementos: dict, texto: str) -> str:
    """
    PRE: "info_elementos"  es un dict con los datos de las carpetas o archivos segun 
    corresponda
    
    POST: devuelve el string "id_elemento" con id del elemento y el str "nomrbe_elemento" 
    con su nombre
    """
    if info_elementos:
        print(texto)
                        #info_elementos.keys() es {1,2,3... correspondiente a cada ele
        num_ele = int(validar_opcion( min( info_elementos.keys() ), max ( info_elementos.keys() ) ) )
        
        id_elemento =  info_elementos[num_ele][1]
        nombre_elemento = info_elementos[num_ele][0] 

    else:
        print('Esta vacio ves? No hay monstruos aqui. Seleccione volver atras.')
        id_elemento = 'root'

    return id_elemento, nombre_elemento





def guardar_paths(info_carpetas: dict, paths: dict) -> dict:
    """
    PRE: "info_carpetas" ( {num_ele: [nombre_carpeta, id_carpeta]} ) es un diccionario y 
    paths ({nombre_carpeta: id_carpeta } )
    
    POST: No devuelve nada. Modifica por parametro el diccionario paths cargandole los datos 
    de info_carpetas, colocando como clave el nombre de la carpeta y como valor su 
    respectivo id
    """
    for info_carpeta in info_carpetas.values():
        nombre_carpeta = info_carpeta[0]
        id_carpeta = info_carpeta[1]

        if nombre_carpeta not in paths.keys():
            paths[nombre_carpeta] = id_carpeta


def mostrar_elementos(info_elementos: dict, tipo_ele: str):
    """
    PRE: "info_elementos" es un diccionario con numeros de elemento como clave, y con
    listas como valores que contienen en la primera posicion los nombres de los elementos
    y en las segunda, sus respectivos.
    
    POST: No devuelve nada solo muestra por panatalla los elementos solicitados.
    """
    for num_ele, elemento in info_elementos.items():
        print (f'{num_ele}-{elemento[0]}')
    
    if info_elementos: #debo preguntarlo porque si esta vacio, tira error
        print(f'Se encontraron {num_ele} {tipo_ele}\n')


def guardar_info_elementos(elementos: dict, info_carpetas:dict, info_archivos):
    """
    PRE: recibe los diccionarios "elementos":
    [{id: 'id_elemento', name: 'nombre del elemento', mimeType: '(el tipo de archivo q sea'}]
    "info_carpetas"  {num_carp:['nombre carpeta','id carpeta']} y
    "info_archivos" {num_arch: ['nombre archivo', 'id archivo']}.
    
    POST: No devuelve nada. Modifica por parametro los diccionario "info_carpetas" e 
    "info_archivos" colocando como clave los nombres de los elementos y sus id's como valores.
    """
    num_arch = 0
    num_carp = 0
    for elemento in elementos:
        if elemento['mimeType'] == 'application/vnd.google-apps.folder':
            num_carp += 1
            info_carpetas[num_carp] =   [ elemento['name'], elemento['id'] ]
            #print(elemento['parents']) #testing
        else:
            num_arch += 1
            info_archivos[num_arch] =  [elemento['name'], elemento['id'] ] 
            #print(elemento['parents']) #testing


#LISTAR ELEMENTOS EL REMOTO
def listar_elementos(query: str) -> tuple:
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
                                            fields='nextPageToken, files(id, name, mimeType, parents)',
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

    print('1-Busqueda manual (lista todas las carpetas y archivos disponibles)')
    print('2-Busqueda personalizada (busqueda con palara clave)')
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


def consultar_elementos():
    """
    PRE:

    POST: Redirige a otras funciones de filtro y busqueda de archivos.
    """
    
    print('BUSCADOR DE DRIVE')
    print('--root/Directorio principal--')
    cortar = False
    id_elemento = 'root'
    paths = {'root':'root'}
    while not cortar:

        query = armado_de_consulta(id_elemento)
        info_carpetas, info_archivos = listar_elementos(query)

        print('CARPETAS')
        mostrar_elementos(info_carpetas, 'carpetas')

        print('ARCHIVOS')
        mostrar_elementos(info_archivos,'archivos')

        guardar_paths(info_carpetas, paths) #el objeto de esta funcion es guaradr los paths
                                #xa q el usario pueda volver hacia atras al navegar entre carpetas
        generador_de_id_()
        
        print('1-Abrir una carpeta\n2-Descargar un archivo o carpeta\n3-Atras')
        opc = int( validar_opcion(1,3) )
        if opc == 1:     
            texto ='seleccione la carpeta que desea abrir'
            id_elemento, nombre_elemento = seleccionar_elementos(info_carpetas, texto)
        elif opc == 2:
            texto ='seleccione el archivo o carpeta que desea descargar'
            id_elemento, nombre_elemento = seleccionar_elementos(info_elementos, texto)
        
        if opc in (1,2):    
            

        else:      
            id_elemento, nombre_elemento = retroceder(paths)
         
        print(f'--- {nombre_elemento} ---')
        

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
