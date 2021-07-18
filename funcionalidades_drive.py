import os
import io
from typing import Text
from service_drive import obtener_servicio as service
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import pathlib
import datetime

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


def retroceder(paths: dict) -> tuple:
    """
    PRE: Recibe el diccionario "paths" que tiene como claves los nombres de las carpetas por 
    las que ya se navego el usuario y como valores sus respectivos ids
    
    POST: Devuelve una tupla con los str "id_carpeta" con el id de la carpeta seleccionada
    y "nombre_carpeta" con el nombre de dicha carpeta  
    """
    print('Ingrese el nombre de la carpeta a la que desea retroceder: ')
    for carpeta in paths.keys():
        print(f'-{carpeta}')
    
    nombre_carpeta = input('Su ingreso: ')
    while nombre_carpeta not in paths.keys():
        nombre_carpeta = input('Por favor elija una carpeta de las listadas: \n')

    #print(f'---{nombre_carpeta}---')

    id_carpeta = paths[nombre_carpeta]

    return id_carpeta, nombre_carpeta


def seleccionar_elementos(info_elementos: dict, texto: str) -> str:
    """
    PRE: "info_elementos"  es un dict con los datos de las carpetas o archivos segun 
    corresponda
    
    POST: devuelve el string "id_elemento" con id del elemento y el str "nomrbe_elemento" 
    con su nombre
    """
    print(texto)
                    #info_elementos.keys() es {1,2,3... correspondiente a cada ele
    num_ele = int(validar_opcion( min( info_elementos.keys() ), max ( info_elementos.keys() ) ) )
    
    id_elemento =  info_elementos[num_ele][1]
    nombre_elemento = info_elementos[num_ele][0] 

    return id_elemento, nombre_elemento


def descargar_archivo_binario(id_elemento):
     
    request = service().files().get_media(fileId = id_elemento)
    fh = io.BytesIO()
   
    return fh

def descargar_carpeta(id_elemento):
    
    page_token = None
    cortar = False
    while not cortar:
        resultados = service().files().list(q= f" '{id_elemento}' in parents",
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name, mimeType)',
                                                pageToken= page_token).execute()
        elementos = resultados['files']
        for elemento in elementos:
            id_elemento = elemento['id']
            nombre_elemento = elemento['name']
            mimeType = elemento['mimeType']
            ruta = os.getcwd()
            #request = service().files().export_media(fileId = id_elemento)
            fh = io.BytesIO()
            if mimeType == 'application/vnd.google-apps.folder':
                os.mkdir( ruta + '/' + carpeta_actual)
                carpeta_actual = nombre_elemento
                fh = descargar_carpeta(id_elemento)
            else:
                with open(os.path.join(carpeta_actual,nombre_elemento), 'wb') as arch:
                    arch.write(fh.read())

        page_token = resultados.get('nextPageToken')
        if page_token is None:
            cortar = True
    #request = service().files().export_media(fileId = id_elemento,
    #                                        mimeType = mimeType)
    return fh

def descargar_elemento(info_carpetas: dict, info_archivos: dict) -> None:
    """
    PRE: recibe los diccionarios info_carpetas" e "info_archivos" con el numero de elemento,
    el nombre y su respectivo id

    POST: Devuelve el id y el nombre del elemento descargado. 
    Permite descargar el archivo o carpeta seleccionado en drive por el usuario. 
    """
    pass
    print('1-Carpeta\n2-Archivo')
    opc = int( validar_opcion(1,2))        
    if opc == 1:
        texto = 'seleccione la carpeta que desea descargar' 
        info_elementos = info_carpetas                  
        #mimeType = 'application/vnd.google-apps.folder' # to export files
    else:
        texto = 'seleccione el archivo que desea descargar'
        info_elementos = info_archivos
    
    id_elemento, nombre_elemento = seleccionar_elementos(info_elementos, texto) 
    
    #!!!!!!FUNCION DD ALGUIEN XA NAVEGAR X ARCHIVOS LOCALES!!!!
    #ubicacion = input ('Ingrese la direccion en la que desea guardar el archivo: ')
    ubicacion = ''
        
    #fh = descargar_archivo_binario(id_elemento)
    fh = descargar_carpeta(id_elemento)

    with open(os.path.join(ubicacion,nombre_elemento), 'wb') as arch:
        arch.write(fh.read()) 

    return id_elemento, nombre_elemento


def generador_de_id_elemento(info_carpetas: dict, info_archivos:dict, paths:dict) -> str:
    """
    PRE:
    POST: Devuelve una tupla con el str "id_elemento" con el id del elemento y 
    el str "nombre_elemento" con el nombre del elemento con el q se desea realizar 
    una operacion
    """
    print('1-Abrir una carpeta\n2-Descargar un archivo o carpeta\n3-Atras')
    opc = int( validar_opcion(1,3) )
    if opc == 1 and info_carpetas:      #si la carpeta no esta vacia
        texto ='Seleccione la carpeta que desea abrir'
        info_elementos = info_carpetas
        id_elemento, nombre_elemento = seleccionar_elementos(info_elementos, texto) 
        #print(f'\n--- {nombre_elemento} ---')    
    
    elif opc == 2:
        id_elemento, nombre_elemento = descargar_elemento(info_carpetas, info_archivos)
        print(f'se ha descargado {nombre_elemento}')
        nombre_elemento = 'root' #Xq quiero, lo redirijo a root xa que continue desde ahi

    else: #retroceder
        print('Esta vacio ves? No hay monstruos aqui')
        id_elemento, nombre_elemento = retroceder(paths)
           
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
        query = f" '{id_elemento}' in parents and (not trashed) " 

    else:
        #print('\nQue desea buscar?\n1-Carpetas\n2-Archivos')
        #opc = int(validar_opcion(1,2))
        palabra = input('ingerse palabra clave COMPLETA: ')  #contains solo busca palabras completas no letras!
        query = f" '{id_elemento}' in parents and fullText contains '{palabra} and (not trashed)' " 

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
        
        id_elemento, nombre_elemento = generador_de_id_elemento(info_carpetas, info_archivos, paths)
        
        print(f'---{nombre_elemento}---\n'.ljust(10))
        
        print('Desea continuar buscando?\n')
        print('1-Si\n2-Seleccionar carpeta (Solo para subida de archivo)')
        opc = int(validar_opcion(1,2))
        if opc == 2:
            cortar = True

    return id_elemento, nombre_elemento

def seleccionar_archivo_subida():
    print('Seleccione el archivo o carpeta de su computadora que desea subir')
    #MODULO DE ALGUIEN XA BUSCAR ARCHUVOS EN LOCAL
    pass


def subir_archivos(ruta_archivo):
    
    #ruta_archivo = seleccionar_archivo_subida()
    #ruta_archivo = 'prueba_xa_subir.txt'
        
    print('Selccione la carpeta a la que desea subir el archivo')
    carpeta_id, nombre_elemento = consultar_elementos()
    
    
    file_metadata = {
                    'name': ruta_archivo,
                    'parents': [carpeta_id]
                }
 
    media = MediaFileUpload(ruta_archivo)

    file = service().files().create(body = file_metadata,
                                        media_body = media,
                                        fields = 'id').execute()
    
    print (f'Se subio correctamente: {ruta_archivo} a {nombre_elemento}')

#subir_archivos()

def crear_archivos(ruta):
    #Funciones en el local para crear el archivo y darme el nombre, 
    #consulto las carpetas para saber a donde lo subo
    #id_elemento, nombre_elemento = consultar_elementos()
    #creo el archivo con metodo create en id_elemento q traje de la busqueda

    #crear carpetas
    #
    rutas_archivos = [ruta]
    for ruta in rutas_archivos:

        if not os.path.isfile(ruta): # si no es un archivo (=> es una carpeta)

            nombre_archivo = ruta   
            file_metadata = {
                'name': nombre_archivo,
                'mimeType': 'application/vnd.google-apps.folder'
                        }

            file = service().files().create(body=file_metadata,
                                            fields='id').execute()
            
            #print 'Folder ID: %s' % file.get('id')
        
            id_carpeta = file.get('id')
        
        else:
            #create file in a folder

            folder_id = '0BwwA4oUTeiV1TGRPeTVjaWRDY1E'
            file_metadata = {
            'name': 'photo.jpg',
            'parents': [folder_id]
                }
            media = MediaFileUpload('files/photo.jpg',
                                mimetype='image/jpeg',
                                resumable=True)
            
            file = service().files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
            #print 'File ID: %s' % file.get('id')

    #print(f'se creo correctamente {} en {id_elemento}')

#crear_archivos()

def remplazar_archivos(arch, id_ele):
    
    media = MediaFileUpload(arch)

    service().files().update(fileId = id_ele,
                                    media_body = media).execute()
                                    
                                                        
def sincronizar():
    # for i in list(pathlib.Path().iterdir()):
    #     print(i)
    #     fname = pathlib.Path(i)
    #     print(fname.stat().st_ctime)
    #     ctime = datetime.datetime.fromtimestamp(fname.stat().st_ctime)
    #     #assert fname.exists(), f'No such file: {fname}'  # check that the file exists
    #     print(ctime)
    
    #cargo y creo el siguiente dict
    #arch_locales_sinc = {nombre_arch: modifiedTime}
    arch_locales_sinc = dict()

    arch = 'archivo_xa_actualizar.txt'
    fname = pathlib.Path(arch)
    ctime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
    print(ctime)
    
    page_token = None
    cortar = False
    id_carpeta = '1IgwMubXSE_XlBgoSF7pgGS_AL8w2ex6i'
    while not cortar:
        #files().list() devuelve un diccionario de diccionarios, q guardo en "resultados"
        resultados = service().files().list(q= f" '{id_carpeta}' in parents and (not trashed) ",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name, modifiedTime)',
                                            pageToken=page_token).execute()
        #print(resultados)  #testing
        #En el dict resultados, una clave es 'files', que es una lista de diccionarios donde 
        #cada diccionario es un elemento de dicha lista. Lo guardo en elementos.
        
        elementos = resultados['files']

        #print(elementos) #testing
        #guardar_info_elementos(elementos, info_carpetas, info_archivos)
        for elemento in elementos:
            #print(elemento['modifiedTime']) 
            print(elemento)
            print(elemento['modifiedTime'])
            id_ele = elemento['id']
        print(id_ele)
        #chequeo si hay mas resultados
        page_token = resultados.get('nextPageToken')
        if page_token is None:
            cortar = True
    
    #OJO !!! Al caegar la fecha de modif hay q formatearla xq viene en horario yanqui
    #arch_remotos_sinc = {nombre_arch: [id_ele, modifiedTime]}
    arch_remotos_sinc = dict()
    for arch_local, fecha_local in arch_locales_sinc.items():
        for arch_remoto, info_arch in arch_remotos_sinc.items():
            fecha_remoto = arch_remotos_sinc[arch_remoto][1]
            if fecha_remoto != fecha_local:  
                id_arch = arch_remotos_sinc[0]
                remplazar_archivos(arch_local, id_arch)
                
                print(f'se actualizo {arch_local} correctamente')
    
        
#sincronizar()
consultar_elementos()