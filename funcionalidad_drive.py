import os
import io
from typing import Dict, Text
import typing
from service_drive import obtener_servicio as service
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import pathlib
import datetime

def validar_opcion(opc_minimas: int, opc_maximas: int, texto: str = '') -> str:
    """
    PRE: Recibe los int "opc_minimas" y "opc_maximas" que 
    simbolizan la cantidad de opciones posibles.

    POST: Devuelve en formato string la var "opc" con un número 
    entero dentro del rango de opciones.
    """
    opc = input(" -> {}".format(texto))
    while not opc.isnumeric() or int(opc) > opc_maximas or int(opc) < opc_minimas:
        opc = input("Por favor, ingrese una opcion valida: ")
    
    return opc


def retroceder(paths: list) -> tuple:

    """
    PRE: Recibe la lista "paths" con info sobre las carpetas por las que
    ya navego el usuario:
    "paths" =[ [nombre_carpeta, id_carpeta], ]
    
    POST: Devuelve los str "id_carpeta" y " nombre_carpeta" para retroceder
    a dicha carpeta.
    """  
    ultima_carpeta = paths.pop() #saco la ultima que eleji

    if paths: # si no queda vacia depues del pop
        nombre_carpeta = paths[-1][0]   #devuelvo el nombre
        id_carpeta = paths[-1][1] #y id de la anterior en la que estuve SIN SACARLO
    
    else: #si queda vacia, la cargo de nuevo
        paths.append(['Directorio principal(root)','root'])
        id_carpeta, nombre_carpeta = 'root', 'Directorio principal(root)'
            
    return id_carpeta, nombre_carpeta


def seleccionar_elementos(info_elementos: dict) -> str:
    """
    PRE: Recibe el diccionario "info_elementos" con info sobre
    carpetas o archivos segun corresponda:
    info_elementos = { num_elemento: ['nombre elemento', 'id elemento', ['id parents'], 
    'mimeType' ] }

    POST: devuelve los str "id_elemento", "nombre_elemento", "id_parents", "mime_type" 
    
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
    PRE: Recibe los diccionarios "info_carpetas" e "info_archivos":
    info_carpetas = { num_carpeta: ['nombre carpeta', 'id carpeta', ['id parents'], 
    'mimeType' ] }
    info_archivos = { num_archivo: ['nombre archivo', 'id elemento', ['id parents'], 
    'mimeType' ] }
    y la lista "paths":
    paths =[ [nombre_carpeta, id_carpeta], ]

    POST: Permite retroceder a la carpeta si se elije esa opcion.
    Devuelve una 4-upla con 4 str: "id_elemento", "id_elemento", "nombre_elemento",
    "id_parents", "elemento", "mime_type".
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


def mostrar_elementos(info_elementos: dict, tipo_ele: str):
    """
    PRE: Recibe el diccionario "info_elementos" que puede contener informacion
    de carpetas o archivos:
    info_elementos = { num_elemento: ['nombre elemento', 'id elemento', ['id parents'], 
    'mimeType' ] }

    POST: No devuelve nada solo muestra por panatalla los elementos del diccionario.
    """
    for num_ele, elemento in info_elementos.items():
        print (f'{num_ele}-{elemento[0]}')
    
    if info_elementos: #debo preguntarlo porque si esta vacio, tira error
        print(f'Se encontraron {num_ele} {tipo_ele}\n')
    else:
        print(f'No se encontraron {tipo_ele}\n')


def ordenar_info_elementos(elementos: dict) -> dict:
    """
    PRE: Recibe el diccionario "elementos" que puede conetener 
    "carpetas" o "archivos":
    elementos = {nombre_elemento: ['id elemento', 'fecha_modif', ['id_parents'], 'mimeType'] }

    POST: Crea y devuelve el diccionario "info_elementos" que
    puede contener "carpetas" o "archivos":
    info_elementos = {num_elemento: ['nombre elemento','id elemento', ['id parents'], 
    'mimeType' ]}
    
    """
    info_elementos = dict()
    num_ele = 0
    for nombre_elemento, info_elemento in elementos.items():
        num_ele += 1                 #name           #id                #2
        info_elementos[num_ele] =   [nombre_elemento, info_elemento[0], info_elemento[2], info_elemento[3]]
    
    return info_elementos


def guardar_info_elementos(elementos: dict, carpetas:dict, archivos:dict):
    """
    PRE: Recibe la lista de diccionarios (cada diccionario es un elemento): 
    elementos = [{id: 'id_elemento', name: 'nombre del elemento', 'mimeType': 'txt/plain(por ej)', 
    'modifiedTime': 'fecha de modif','parents': ['id_parents'] } ],
    
    y los diccionarios "carpetas" y "archivos":
    carpetas = {nombre_carpeta: ['id carpeta', 'fecha_modif', '[id_parents'], 'mimeType' ]} y
    archivos =  {nombre_carpeta: ['id carpeta', 'fecha_modif', ['id_parents'], 'mimeType' ]}.
    
    POST: No devuelve nada. Modifica por parametro los diccionarios "carpetas" y
    "archivos" colocando como claves los nombres de los elementos y su informacion en una lista
    como valores.
    """
    for elemento in elementos:
        if elemento['mimeType'] == 'application/vnd.google-apps.folder':
            #chequea q no existe
            carpetas[ elemento['name'] ] = [elemento['id'], elemento['modifiedTime'], elemento['parents'], elemento['mimeType']]
            #print(elemento['parents']) #testing
        else:
            archivos[ elemento['name'] ] = [elemento['id'], elemento['modifiedTime'], elemento['parents'], elemento['mimeType']]
            print(elemento['parents']) #testing


def listar_elementos(query: str) -> tuple:
    """
    PRE: Recibe el string "query" con la consulta a enviar a la API de drive.

    POST: Devuelve los diccionarios "carpetas" y "archivos":
    carpetas = {nombre_carpeta: ['id carpeta', 'fecha_modif', ['id_parents'], mimetype ]} y
    archivos = {nombre_carpeta: ['id carpeta', 'fecha_modif', ['id_parents'], mimetype ]}.
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
    PRE: Recibe el str "id_elemento" con el id de la carpeta o archivo que selecciono 
    el usurario
    
    POST: devuelve el string "query" con la consulta a buscar en el drive
    """

    print('0- LISTA TODO MYDRIVE ')
    print('1- Busqueda por numero')
    print('2- Busqueda por palabra (Escribir palabra clave : palabra COMPLETA )')
    print("----> ej - archivo -> '< nombre archivo >.< extension >' ")
    print("----> ej - carpeta -> '< nombre carpeta >' ")
    print("3 - Volver al menu principal ")
    opc = int(validar_opcion(0,3)) 

    cortar = False
    #opc == o -> listar todo giuardar todo
    if opc == 0:
        query = "not trashed"

    elif opc == 1:
        query = f" '{id_elemento}' in parents and (not trashed) " 

    elif opc == 2:
        #print('\nQue desea buscar?\n1-Carpetas\n2-Archivos')
        #opc = int(validar_opcion(1,2))
        palabra = input('ingerse palabra clave COMPLETA: ')  #contains solo busca palabras completas no letras!
        query = f" '{id_elemento}' in parents and fullText contains '{palabra} and (not trashed)' " 

        print(query) #testing
    
    elif opc == 3:
        query = ""
        cortar = True

    
    return query, cortar


def consultar_elementos():
    """
    PRE: No recibe nada. Funciona como un menu gestor de drive

    POST: Redirige a otras funciones de filtro y busqueda de archivos. 
    Devuelve los str "id_elemento", "nombre_elemento", "id_parents", "mime_type"
    """
    print('BUSCADOR DE DRIVE'.rjust(50))
    print('--- My Drive -> Directorio principal---'.rjust(57))
    cortar = False
    

    nombre_elemento = "directorio_principal('root')"
    id_elemento = 'root'
    paths = [[nombre_elemento, id_elemento]]


    while not cortar:

        query, cortar = armado_de_consulta(id_elemento)
        if not cortar:
            carpetas, archivos = listar_elementos(query)

            info_carpetas = ordenar_info_elementos(carpetas)
            info_archivos = ordenar_info_elementos(archivos)

            print('CARPETAS')
            mostrar_elementos(info_carpetas, 'carpetas')

            print('ARCHIVOS')
            mostrar_elementos(info_archivos,'archivos')

            id_elemento, nombre_elemento, id_parents, elemento, mime_type = generador_de_id_elemento(info_carpetas, info_archivos, paths)
            
            if elemento == 'carpeta':
                paths.append([nombre_elemento, id_elemento])
                print('1-Abrir carpeta\n2-Selccionar elemento')
                opc = int(validar_opcion(1,2))        
            
            elif elemento == 'retroceder':
                opc = 1
            
            else:           #es un archivo
                opc = 2

            if opc == 2:
                cortar = True
            
            else:
                ruta = ""
                for carpeta in paths:
                    ruta += " -> " + carpeta[0]

                print(f"Historial: {ruta}\n") 
                print(f'---{nombre_elemento}---\n'.rjust(50))
        else:
            id_elemento = ""
            nombre_elemento = ""
            id_parents = ""
            mime_type = ""


    return id_elemento, nombre_elemento, id_parents, mime_type


def validar_elemento(elemento):
    """
    PRE:Recibe el str "elemento" con el tipo de elemento a validar. Este puede ser
    "carpeta" o "archivo"
    
    POST: Redirige a consultar elementos hasta el fin de la especie humana o hasta el 
    devolver una carpeta o archivo segun corresponda.
    Devuelve los str "id_elemento", "nombre_elemento", "id_parents"
    """
    mime_type_carpeta = 'application/vnd.google-apps.folder'
    id_elemento, nombre_elemento, id_parents, mime_type = consultar_elementos()

    if elemento == 'carpeta':
        while mime_type != mime_type_carpeta:
            print('Por favor elija una carpeta')
            id_elemento, nombre_elemento, id_parents, mime_type = consultar_elementos()
    
    else:   # necesito un archivo
        while mime_type == mime_type_carpeta or mime_type == "":
            print('Por favor elija un archivo')
            id_elemento, nombre_elemento, id_parents, mime_type = consultar_elementos()

    return id_elemento, nombre_elemento, id_parents

def descargar_archivo_binario(id_elemento, nombre_elemento):
    """
    PRE: Recibe el str "id_elemento" con el id del archivo a descargar

    POST: Descarga el archivo cuyo id es el indicado y
    devuelve el objeto "arch" con el archivo q se descargo
    """
     
    request = service().files().get_media(fileId = id_elemento)
    arch = io.BytesIO()
    
    return arch

def descargar_carpeta(id_elemento, nombre_elemento, ruta_actual):
    """
    Recibe los str "id_elemento" , "nombre_elemento"  y "ruta_actual"

    POST: No devuelve nada. Descarga la carpeta, subcarpetas y archivos que
    se encuentren en la carpeta seleccionada.
    """
    ruta_actual = ruta_actual + "/" + nombre_elemento
    os.mkdir(ruta_actual)
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
            fh = io.BytesIO()

            if mimeType == 'application/vnd.google-apps.folder':
                descargar_carpeta(id_elemento,nombre_elemento, ruta_actual)
            else:
                with open(os.path.join(ruta_actual,nombre_elemento), 'wb') as arch:
                    arch.write(fh.read())

        page_token = resultados.get('nextPageToken')
        if page_token is None:
            cortar = True
    #request = service().files().export_media(fileId = id_elemento,
    #                                        mimeType = mimeType)

def menu_descargar_elementos(ruta_local) -> None: #en proceso......!!!!!!
    """
    PRE: recibe el str "ruta_local" con la ruta local en la que esta paardo el usuario

    POST: Redirige a otras funciones para permitir descargar el archivo o carpeta
    seleccionado en drive por el usuario. 
    """
    print('\n ------------- MENU DESCARGAR ------------- ')
    print('Que desea descargar?')
    print('1-Carpeta\n2-Archivo')
    opc = int( validar_opcion(1,2))        
    if opc == 1:
        print('seleccione la carpeta que desea descargar')

        id_carpeta, nombre_elemento, id_parents = validar_elemento('carpeta')    

        descargar_carpeta(id_carpeta,nombre_elemento,ruta_local)
        print()
        print(f'se descargo correctamente "{nombre_elemento}"\n')              
    
    else: #descargar un archivo
        print('seleccione el archivo que desea descargar')
        
        id_archivo, nombre_elemento, id_parents = validar_elemento('archivo')

        arch = descargar_archivo_binario(id_archivo, nombre_elemento)
        
        print(f'se descargo correctamente "{nombre_elemento}"\n')              

        #!!!!!!FUNCION DD ALGUIEN XA NAVEGAR X ARCHIVOS LOCALES!!!!
        #ubicacion = input ('Ingrese la direccion en la que desea guardar el archivo: ')
        # ubicacion = ruta_local
        # # escribir todo lo q venga en arch
        # with open(os.path.join(ubicacion,nombre_elemento), 'wb') as archivo:
        #     archivo.write(arch.read()) 

def subir_archivos(nombre_archivo, ruta_archivo: str, carpeta_id: str) -> None:
    """
    PRE:Recibe los str "nombre_archivo", "ruta_archivo" y "carpeta_id"
    
    POST: No devuelve nada. Sube los archivos a la carpeta indicadas.
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
    PRE: Recibe el str "carpeta_contenedora" con el nombre de la carpeta en
    la que esoy parado en el local

    POST: Busca entre los nombres de las carpetas del remoto la carpeta
    correspondiente a la que me encuentro en el local y 
    devuelve los str "carpeta_id" y "nombre_carpeta"
    """    
    #primero listo todas las carpetas de la nube
    print(carpeta_contenedora)
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
    PRE: Recibe los str "nombre_archivo", "ruta_archivo" y "carpeta_contenedora"

    POST: No devuelve nada. Funciona como menu intermedio para permitirle subir 
    archivos a una carpeta a eleccion del usuario.
    """    
    print('SUBIR ARCHIVOS')
    print('1-Subir a carpeta homonima en drive\n2-Elegir otra carpeta')
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
    eleccion = input("1 - MyDrive\n2 - Otra Carpeta \n ->  ")

    if eleccion == "1":
        subir_archivos(nombre_archivo, ruta_archivo, "root")
    elif eleccion == "2":
        opciones_subir_archivos(nombre_archivo, ruta_archivo, carpeta_contenedora)


def remplazar_archivos(ruta_archivo, id_archivo):
    """
    PRE: Recibe los str "ruta_arch" y "id_arch"
    
    POST: No devuelve nada. Reemplaza en la nube el archivo de id "id_archivo" 
    por el archivo que se encuentra en "ruta_archivo"
    """
    media = MediaFileUpload(filename = ruta_archivo)

    service().files().update(fileId = id_archivo,
                            media_body = media).execute()


def mover_archivos():

    """
    PRE: No recibe parametros.

    POST: No devuelve nada. Permite mover archivos de a uno a la vez de una carpeta
    a otra en drive
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