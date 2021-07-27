
import os
import io
from typing import Dict, Text
#from typing import overload, union
import typing
from service_drive import obtener_servicio as service
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import pathlib
import datetime


#FALTA: 
#   1)-- VALIDAR SI LO Q TRAIGO ES CARPETA O ARCHIVO ===> VOLER A MODIFCAR info_carpetas, info_archivos
#xa q traigan el mimetype. Crear funcion, validar mimetype, q va a ser solo un ciclos que
# llama a consultar_elementos() hasta q el mimetype deja de ser ( o es) una carpeta.
# parametros: mimetype, y adentro llama a consultar_elementos(). Asi valido todas las cosas
#q bajo de la nube
#   2)Hacer menu descargar_carpeta y chequear decargar carpeta
#   3)Chequear con csv's y dict la creacion de carpetas anidadas.


def validar_opcion(opc_minimas: int, opc_maximas: int, texto: str = '') -> str:
    """
    PRE: "opc_minimas" y "opc_maximas" son dos números enteros que 
    simbolizan la cantidad de opciones posibles.
    POST: Devuelve en formato string la var "opc" con un número 
    entero dentro del rango de opciones.
    """
    opc = input(" -> {}".format(texto))
    while not opc.isnumeric() or int(opc) > opc_maximas or int(opc) < opc_minimas:
        opc = input("Por favor, ingrese una opcion valida: ")
    
    return opc


def retroceder(paths: dict) -> tuple:     #VER CON PILAAAAAAAAA!!!!1 

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

    id_carpeta = paths[nombre_carpeta]

    return id_carpeta, nombre_carpeta


def seleccionar_elementos(info_elementos: dict) -> str:
    """
    PRE: "info_elementos"  es un dict con los datos de las carpetas o archivos segun 
    corresponda
    
    POST: devuelve el string "id_elemento" con id del elemento y el str "nomrbe_elemento" 
    con su nombre
    
    info_carpetas = {num_carp:['nombre carpeta','id carpeta', ['id parents'], 'mimeType' ]}
    
    """
    texto = 'cual?: '
                    #info_elementos.keys() es {1,2,3... correspondiente a cada ele
    num_ele = int(validar_opcion( min( info_elementos.keys() ), max ( info_elementos.keys() ), texto ) )
    
    nombre_elemento = info_elementos[num_ele][0]
    id_elemento =  info_elementos[num_ele][1]
    id_parents =  info_elementos[num_ele][2]
    mime_type = info_elementos[num_ele][3]
    
    print(f'se ha seleccionado {nombre_elemento}')

    return id_elemento, nombre_elemento, id_parents, mime_type


def generador_de_id_elemento(info_carpetas: dict, info_archivos:dict, paths:dict) -> tuple:
    """
    PRE:
    POST: Devuelve una tupla con el str "id_elemento" con el id del elemento y 
    el str "nombre_elemento" con el nombre del elemento con el q se desea realizar 
    una operacion
    """
    print('1-Seleccionar una carpeta\n2-Seleccionar un archivo\n3-Atras')
    opc = int( validar_opcion(1,3) )
    if opc == 1 and info_carpetas:  #si hay carpetas para seleccionar
        elemento = 'carpeta'
        id_elemento, nombre_elemento, id_parents, mime_type = seleccionar_elementos(info_carpetas)

    elif opc == 2 and info_archivos:  #archivos
        elemento = 'archivo'
        id_elemento, nombre_elemento, id_parents, mime_type = seleccionar_elementos(info_archivos)
        
    else: #retroceder
        elemento = 'retroceder'
        id_elemento, nombre_elemento = retroceder(paths)
        id_parents = []
        mime_type = 'application/vnd.google-apps.folder'
    
    return id_elemento, nombre_elemento, id_parents, elemento, mime_type


def guardar_paths(info_carpetas: dict, paths: dict) -> dict: #VER CON PILAAAAAA!!!
    """
    PRE: "info_carpetas" ( {num_ele: [nombre_carpeta, id_carpeta, ['id_parents'], 'mimeType' ] } ) es un diccionario y 
    paths ({nombre_carpeta: id_carpeta } )
    
    
    POST: No devuelve nada. Modifica por parametro el diccionario paths cargandole los datos 
    de info_carpetas, colocando como clave el nombre de la carpeta y como valor su 
    respectivo id
    """
    for info_carpeta in info_carpetas.values():
        nombre_carpeta = info_carpeta[0]
        id_carpeta = info_carpeta[1]
            #mejorar con pila LIFO con una lista usando append y pop. 
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
    else:
        print(f'No se encontraron {tipo_ele}\n')


def ordenar_info_elementos(elementos: dict):
    """
    PRE: recibe el diccionario "elementos" que puede ser:
    "carpetas"  {nombre_carpeta: ['id carpeta', 'fecha_modif', ['id_parents'], 'mimeType'  ]} y
    "archivos" {nombre_carpeta: ['id carpeta', 'fecha_modif', ['id_parents'], 'mimeType' ]}.
    POST: Crear y devuelve el diccionario "info_elementos" con esta etsructura:
    {num_carp:['nombre carpeta','id carpeta', ['id parents'], 'mimeType' ]}
    """
    info_elementos = dict()
    num_ele = 0
    for nombre_elemento, info_elemento in elementos.items():
        num_ele += 1                 #name           #id                #2
        info_elementos[num_ele] =   [nombre_elemento, info_elemento[0], info_elemento[2], info_elemento[3]]
    
    return info_elementos


def guardar_info_elementos(elementos: dict, carpetas:dict, archivos:dict):
    """
    PRE: recibe los diccionarios "elementos":
    [{id: 'id_elemento', name: 'nombre del elemento', mimeType: '(el tipo de archivo q sea'},
    'modifiedTime': 'fecha de modif','parents': ['id_parents']]
   
    "carpetas"  {nombre_carpeta: ['id carpeta', 'fecha_modif', '[id_parents'], 'mimeType' ]} y
    "archivos" {nombre_carpeta: ['id carpeta', 'fecha_modif', ['id_parents'], 'mimeType' ]}.
    
    POST: No devuelve nada. Modifica por parametro los diccionario "info_carpetas" e 
    "info_archivos" colocando como clave los nombres de los elementos y sus id's y fecha de modif
    en una lista como valores.
    """
    for elemento in elementos:
        if elemento['mimeType'] == 'application/vnd.google-apps.folder':
            #chequea q no existe
            carpetas[ elemento['name'] ] = [elemento['id'], elemento['modifiedTime'], elemento['parents'], elemento['mimeType']]
            #print(elemento['parents']) #testing
        else:
            archivos[ elemento['name'] ] = [elemento['id'], elemento['modifiedTime'], elemento['parents'], elemento['mimeType']]
            print(elemento['parents']) #testing


#LISTAR ELEMENTOS EL REMOTO
def listar_elementos(query: str) -> tuple:
    """
    PRE: Recibe el string "query" con la consulta a enviar a la API de drive.
    
    POST: Devuelve los diccionarios "carpetas" y "archivos" con los nombres de los 
    "carpetas"  {nombre_carpeta: ['id carpeta', 'fecha_modif', ['id_parents'], mimetype ]} y
    "archivos" {nombre_carpeta: ['id carpeta', 'fecha_modif', ['id_parents'], mimetype ]}.
    """
    page_token = None
    cortar = False

    carpetas = dict()
    archivos = dict()
    while not cortar:
        #files().list() devuelve un diccionario de diccionarios, q guardo en "resultados"
        resultados = service().files().list(q= query,
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name, mimeType, modifiedTime, parents)',
                                            pageToken=page_token).execute()
        #print(resultados)  #testing
        #En el dict resultados, una clave es 'files', que es una lista de diccionarios donde 
        #cada diccionario es un elemento de dicha lista. Lo guardo en elementos.
        
        elementos = resultados['files']
        
        #print(elementos) #testing
        #guardar_info_elementos(elementos, info_carpetas, info_archivos)

        guardar_info_elementos(elementos, carpetas, archivos)
        
        #chequeo si hay mas resultados
        page_token = resultados.get('nextPageToken')
        if page_token is None:
            cortar = True

    #return info_carpetas, info_archivos
    return carpetas, archivos


def armado_de_consulta(id_elemento: str) -> str:
    """
    PRE: "id_elemento" es el id de la carpeta o archivo que selecciono el usurario
    
    POST: devuelve el string "query" con la consulta a buscar en el drive
    """

    print('0- LISTA TODO MYDRIVE ')
    print('1- Busqueda por numero')
    print('2- Busqueda por palabra (Escribir palabra clave : palabra COMPLETA )')
    print("----> ej - archivo -> '< nombre archivo >.< extension >' ")
    print("----> ej - carpeta -> '< nombre carpeta >' ")
    opc = int(validar_opcion(0,2)) 
    #opc == o -> listar todo giuardar todo
    if opc == 0:
        query = " mimeType = 'application/vnd.google-apps.folder' "

    elif opc == 1:
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
    info_carpetas"  {num_carp:['nombre carpeta','id carpeta', ['id_parents'], 'mimeType' ] } y
    "info_archivos" {num_arch: ['nombre archivo', 'id archivo', ['id_parents'], 'mimeType' ] }
    
    Devuelve id_elemento, nombre_elemento, id_parents
    """
    print('BUSCADOR DE DRIVE'.rjust(50))
    print('---root/Directorio principal---'.rjust(57))
    cortar = False
    id_elemento = 'root'
    paths = {'root':'root'}
    while not cortar:

        query = armado_de_consulta(id_elemento)

        carpetas, archivos = listar_elementos(query)

        info_carpetas = ordenar_info_elementos(carpetas)
        info_archivos = ordenar_info_elementos(archivos)

        print('CARPETAS')
        mostrar_elementos(info_carpetas, 'carpetas')

        print('ARCHIVOS')
        mostrar_elementos(info_archivos,'archivos')

        guardar_paths(info_carpetas, paths) #el objeto de esta funcion es guaradr los paths
                            #xa q el usario pueda volver hacia atras al navegar entre carpetas
        
        id_elemento, nombre_elemento, id_parents, elemento, mime_type = generador_de_id_elemento(info_carpetas, info_archivos, paths)
        
        if elemento == 'carpeta':
            print('1-Abrir carpeta\n2-Selccionar elemento')
            opc = int(validar_opcion(1,2))        
        
        elif elemento == 'retroceder':
            opc = 1
        
        else:           #es un archivo
            opc = 2

        if opc == 2:
            cortar = True
        
        else:
            print(f'---{nombre_elemento}---\n'.rjust(50))


    return id_elemento, nombre_elemento, id_parents, mime_type


#consultar_elementos()

def validar_elemento(elemento):
    """
    PRE:Recibe un str con el tipo de elemmento a validar
    
    POST:Redirige a consultar elementos hasta devolver una carpeta o archivo segun corresponda.
    Devuelve: id_elemento, nombre_elemento, id_parents
    """
    mime_type_carpeta = 'application/vnd.google-apps.folder'
    id_elemento, nombre_elemento, id_parents, mime_type = consultar_elementos()

    if elemento == 'carpeta':
        while mime_type != mime_type_carpeta:
            print('Por favor elija una carpeta')
            id_elemento, nombre_elemento, id_parents, mime_type = consultar_elementos()
    
    else:   # necesito un archivo
        while mime_type == mime_type_carpeta:
            print('Por favor elija un archivo')
            id_elemento, nombre_elemento, id_parents, mime_type = consultar_elementos()

    return id_elemento, nombre_elemento, id_parents


#validar_elementos()

def descargar_archivo_binario(id_elemento, nombre_elemento):
     
    request = service().files().get_media(fileId = id_elemento)
    arch = io.BytesIO()
    
    return arch


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
            carpeta_actual = ''
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


def menu_descargar_elementos(ruta_local) -> None: #en proceso......!!!!!!

    """
    PRE: recibe los diccionarios info_carpetas" e "info_archivos" con el numero de elemento,
    el nombre y su respectivo id
    POST: 
    Permite descargar el archivo o carpeta seleccionado en drive por el usuario. 
    """
    print('MENU DESCARGAR')
    print('Que desea descargar?')
    print('1-Carpeta\n2-Archivo')
    opc = int( validar_opcion(1,2))        
    if opc == 1:
        print('seleccione la carpeta que desea descargar')

        id_carpeta, nombre_elemento, id_parents = validar_elemento('carpeta')    
        
        arch = descargar_carpeta(id_carpeta)              
    
    else: #descargar un archivo
        print('seleccione el archivo que desea descargar')
        
        id_archivo, nombre_elemento, id_parents = validar_elemento('archivo')

        arch = descargar_archivo_binario(id_archivo, nombre_elemento)
    
    #!!!!!!FUNCION DD ALGUIEN XA NAVEGAR X ARCHIVOS LOCALES!!!!
    #ubicacion = input ('Ingrese la direccion en la que desea guardar el archivo: ')
    ubicacion = ruta_local
    # escribir todo lo q venga en arch
    with open(os.path.join(ubicacion,nombre_elemento), 'wb') as archivo:
        archivo.write(arch.read()) 

##menu_descargar_elementos()


def subir_archivos(nombre_archivo, ruta_archivo: str, carpeta_id: str) -> None:
    """
    PRE:
    
    POST: No devuelve nada. Sube los archivos a la carpetas indicadas. Esta funcion
    reemplaza crear archivos, pues crear un archivo es subir un archivo vacio.
    """    
    file_metadata = {
                    'name': nombre_archivo,
                    'parents': [carpeta_id]
                }
 
    media = MediaFileUpload(filename = ruta_archivo)

    service().files().create(body = file_metadata,
                                    media_body = media,
                                    fields = 'id').execute()    #creo q esta de mas


def encontrar_carpeta_upstream(carpeta_contenedora: str) -> tuple:
    """
    PRE:
    POST: Compara las carpetas de local y remoto para encontrar la q correspondiente a
    la q me encuentro localmente
    """    
    #primero listo todas las carpetas de la nube
    query = f" mimeType = 'application/vnd.google-apps.folder' and name contains '{carpeta_contenedora}' and not trashed "
    
    carpetas, archivos = listar_elementos(query)
    
    if carpeta_contenedora in carpetas.keys():  #si existe la carpeta en el remoto
        #si coincide con la local lo subo ahi
        for nombre_carpeta, info_carpeta in carpetas.items():
            if nombre_carpeta == carpeta_contenedora:
                carpeta_id = info_carpeta[0]
    else:
        print('La carpeta no existe con este mismo nombre en la nube')
        print('Por favor elija otra carpeta, o cree una nueva')
        carpeta_id = '' #xa q no falle
        nombre_carpeta = '' #xa q no falle

    return carpeta_id, nombre_carpeta


def opciones_subir_archivos( nombre_archivo: str, ruta_archivo: str, carpeta_contenedora: str) -> None:
    """
    PRE:
    POST:No devuelve nada, es un menu intermedio para subir archivos
    """    
    print('SUBIR ARCHIVOS')
    print('1-Subir a misma carpeta en drive\n2-Elegir otra carpeta')
    opc = int(validar_opcion(1,2))
    if opc == 1:
        carpeta_id, nombre_carpeta = encontrar_carpeta_upstream(carpeta_contenedora)
        if carpeta_id != '' and nombre_carpeta != '': #si encontro la carpeta
            subir_archivos(nombre_archivo, ruta_archivo, carpeta_id)
        #else no va, vuelve al menu ppal y da 2 opc. 
        # 1) crear carpeta con 
        # mismo nombre ojo, todavia no puedo subir todos loas archivos. 
        # 2)(pedir nombre y dsps consultar_elmentos(), xa elegir donde crearla
        # y recien manda a crear_carpeta)  
    else:
        print('Selccione la carpeta a la que desea subir el archivo')
        carpeta_id, nombre_carpeta, id_parents = validar_elemento('carpeta')
        #carpeta_id, nombre_carpeta, id_parents, mime_type = consultar_elementos()
        subir_archivos(nombre_archivo, ruta_archivo, carpeta_id)
        
        print (f'Se subio correctamente: {nombre_archivo} a {nombre_carpeta}')


def menu_subir_archivos(ruta_archivo, nombre_archivo, carpeta_contenedora):
    print('Seleccione el archivo o carpeta de su computadora que desea subir')
    eleccion = input("1 - MyDrive\n2 - Otra Carpeta \n ->  ")

    if eleccion == "1":
        subir_archivos(nombre_archivo, ruta_archivo, "root")
    elif eleccion == "2":
        opciones_subir_archivos(nombre_archivo, ruta_archivo, carpeta_contenedora)


#menu_subir_archivos()

def remplazar_archivos(ruta_arch, id_arch):
    """
    PRE: Reemplaza el archivo de string "arch" conociendo su id con el str "id_ele"
    POST:
    """
    media = MediaFileUpload(filename = ruta_arch)

    service().files().update(fileId = id_arch,
                            media_body = media).execute()

def modificar_dic_arch_remoto(archivos_remotos):
    """
    PRE:
    
    POST:
    No devuelve nada. Modufico por referencia el dict "archivos_locales"
    con las sig estructura arch_remotos = { nombre_arch: [id_carpeta, fecha_modif] }
    """
    for archivo_remoto, info_archivo in archivos_remotos.items():
        
        #Modifico la fecha del remoto xa poderla comparar con la local (tambien hasta seg inclusive)
        nueva_fecha_remoto = info_archivo[1][:16].replace('T',' ')          #por error
        archivos_remotos[archivo_remoto][1] = nueva_fecha_remoto

def mover_archivos():

    """
    PRE:
    POST:
    """
    print('Seleccione el archivo que desea mover\n')    
    id_archivo, nombre_arch, id_parents = validar_elemento('archivo')
    
    #id_archivo, nombre_arch, id_parents, mime_type = consultar_elementos()
    
    id_carpeta_salida = id_parents[0]  #ojo q parents es una lista    

    print('\nSeleccione la carpeta a la que desea mover el archivo')
    id_carpeta_destino, nombre_carpeta, id_parents = validar_elemento('carpeta')
    #id_carpeta_destino, nombre_carpeta, id_parents, mime_type = consultar_elementos() 

    service().files().update(fileId = id_archivo,
                        addParents = id_carpeta_destino,
                        removeParents = id_carpeta_salida
                        ).execute()    
    
    print(f'Se movio exitosamente {nombre_arch} a {nombre_carpeta}')  

## ----- SUBIR CARPETAS AL DRIVE ---------------
def crea_carpetas(nombre_carpeta: str, parent: str = "")->str:
    """
    PRE: Recibo la carpeta que quiero subir
    POST: Creo la carpeta en remoto y retorno su id 
    """
    if parent == "":
        file_metadata = {
            "name": nombre_carpeta,
            "mimeType": "application/vnd.google-apps.folder",
            'parents': [] 
        }
    else:
        file_metadata = {
            "name": nombre_carpeta,
            "mimeType": "application/vnd.google-apps.folder",
            'parents': [parent] 
        }
    folder = service().files().create(body = file_metadata).execute()
    id_carpeta = folder.get("id")

    return id_carpeta

def recorrer_carpeta(ruta_actual: str, parent: str = "")->None:
    """
    PRE: Recorro la carpeta en el local
    POST: En caso de leer un archivo lo subo , en caso de leer una carpeta 
          repito el proceso de crear carpeta
    """
    contenido = os.listdir(ruta_actual)
    nombre_carpeta = ruta_actual.split("/")[-1]
    id_carpeta = crea_carpetas(nombre_carpeta, parent)
    for ficheros in contenido :
        if os.path.isfile(ruta_actual + "/" + ficheros):
            ruta_archivo = ruta_actual + "/" + ficheros
            subir_archivos(ficheros, ruta_archivo, id_carpeta)
        else:
            ruta_fichero = ruta_actual + "/" + ficheros
            recorrer_carpeta(ruta_fichero, id_carpeta)

## ----- SINCRONIZAR 

def fecha_modificacion_remoto(id_carpeta: str)->dict:
    """
    PRE: Recibo el id de la carpeta 
    POST: Retorno un dicc con la informacion de cuando fue modificada la carpeta
    """
    ## drive = {nombre fichero = [id fichero , fecha de modificacion]]}
    page_token = None
    drive = dict() # diccionario con {nombre carpeta : [id, mimetype, parent]}
                   # lista_padres es una lista [(padre1, id ), (padre2, id) ... ]
    response = service().files().list(q = f" '{id_carpeta}' in parents and (not trashed) ",
                                    fields='nextPageToken, files(id, name, mimeType,modifiedTime)').execute()
    for file in response.get('files', []):
        file_date = file.get("modifiedTime")[:18].replace('T', ' ')
        drive[file.get("name")] = [file.get("id"),file_date]

    return drive

def fecha_modificacion_local(ruta_actual: str)->tuple:
    """
    PRE: Recibo la ruta donde el usuario esta ubicado
    POST: Retorno una tupla con dos dic, uno que contiene las fechas de modificacion 
        de cada archivo y otra con la modificacion de las carpetas
    """
    ## archivo_fecha_local = {nombre fichero = fecha_modificacion}
    archivos_fechas_local = dict()
    carpetas_fechas_local = dict()
    with os.scandir(ruta_actual) as ficheros:
        for fichero in ficheros:
            if os.path.isfile(fichero):
                fecha_modificacion_archivo = datetime.datetime.fromtimestamp(os.path.getmtime(fichero))
                horas_sumadas = datetime.timedelta(hours = 3)
                fecha_modificacion_archivo += horas_sumadas
                fecha_modificacion_archivo = str(fecha_modificacion_archivo)[:18]
                archivos_fechas_local[fichero.name] = fecha_modificacion_archivo
            elif os.path.isdir(fichero):
                fecha_modificacion_carpeta = datetime.datetime.fromtimestamp(os.path.getmtime(fichero))
                horas_sumadas = datetime.timedelta(hours = 3)
                fecha_modificacion_carpeta += horas_sumadas
                fecha_modificacion_carpeta = str(fecha_modificacion_carpeta)[:18]
                carpetas_fechas_local[fichero.name] = fecha_modificacion_carpeta

    return archivos_fechas_local , carpetas_fechas_local

def descargar_archivo(archivo_id: str, ruta: str)->None:
    """
    PRE: Recibo el id del archivo 
    POST: Descargo el archivo
    """

    print("ruta en funcion descargar_archivo : ", ruta)
    nombre_archivo = ruta

    file_id = archivo_id
    request = service().files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Descarga progres {status.progress() * 100}")

    fh.seek(0)

    with open(nombre_archivo, "wb") as f:
        f.write(fh.read())
        f.close()

def sincronizar(archivos_drive: dict, archivos_local: dict, carpeta_local: dict, ruta: str)->None:
    """
    PRE: Recibo los diccionarios con informacion del remoto y del local 
    POST: Sincronizo cada archivo segun su horario de modificacion
    """

    for archivo , fecha in archivos_local.items():
        if archivo in archivos_drive.keys():
            ruta_archivo = ruta + "/" + archivo
            print(ruta_archivo)
            # comparo fechas 
            if fecha > archivos_drive[archivo][1]:
                print(fecha)
                print(archivos_drive[archivo][1])
                # actualizo el archivo al remoto
                print(ruta_archivo)
                print(archivos_drive[archivo][0])
                remplazar_archivos(ruta_archivo, archivos_drive[archivo][0])
            elif fecha < archivos_drive[archivo][1]:
                print(fecha)
                print(archivos_drive[archivo][1])
                # actualizo archivo al local
                os.remove(ruta_archivo)
                descargar_archivo(archivos_drive[archivo][0], ruta_archivo)

    for carpeta , fecha in carpeta_local.items():
        if carpeta in archivos_drive.keys():
            ruta_archivo = ruta + "/" + carpeta
            # actualizo los archivos dentro de la carpeta
            carpeta_id = encontrar_carpeta_upstream(carpeta)[0]
            archivos_r = fecha_modificacion_remoto(carpeta_id)
            archivos_l = fecha_modificacion_local(ruta_archivo)[0]
            carpeta_l = fecha_modificacion_local(ruta_archivo)[1]
            sincronizar(archivos_r, archivos_l, carpeta_l, ruta_archivo)

