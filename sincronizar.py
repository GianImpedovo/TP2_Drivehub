import pathlib
import datetime
from service_drive import obtener_servicio as service
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

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

    file = service().files().create(body = file_metadata,
                                    media_body = media,
                                    fields = 'id').execute()    #creo q esta de mas
    print(f'se subio bien {nombre_archivo}')



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
            #print(elemento['parents']) #testing

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


def descargar_archivo(id_elemento):
     
    request = service().files().get_media(fileId = id_elemento)
    io.BytesIO()

def descargar_archivo_binario(id_elemento):
     
    request = service().files().get_media(fileId = id_elemento)
    arch = io.BytesIO()

    return arch

def remplazar_archivos(ruta_arch, id_arch):
    """
    PRE: Reemplaza el archivo de string "arch" conociendo su id con el str "id_ele"
    POST:
    """
    media = MediaFileUpload(filename = ruta_arch)

    service().files().update(fileId = id_arch,
                            media_body = media).execute()


def push_local_a_remoto(archivos_locales:dict, archivos_remotos: dict, carpeta_id = "root"):
    """
    PRE:
    POST: No devuelve nada.
    Reemplaza los archivos en el remoto que sufireron modificaciones en el local
    """
    #arch_locales = { nombre_arch: [modifiedTime, ruta_local] }
    #arch_remotos = { nombre_arch: [id_archivo, fecha_modif] }

    for arch_local, info_local in archivos_locales.items():
        if arch_local in archivos_remotos.keys(): #si el nombre del archivo esta en el remoto            
        
            for arch_remoto in archivos_remotos.keys():                
                if arch_local == arch_remoto:   #si coincide el nombre del arch                        
                    fecha_remoto = archivos_remotos[arch_remoto][1]
                    fecha_local = info_local[0] #la fecha es el elemento 0 de la lista 
                    #FALTARIA COMPRARA LINEA A LINEA. Asi no habria q esperar 1 min
                    # pues al comparar linea a linea no deberia saltar => no se modifica
                    if fecha_remoto < fecha_local:  #chequeo la fecha, si es distinta                        
                        id_arch = archivos_remotos[arch_remoto][0]
                        remplazar_archivos(info_local[1], id_arch)
                                    #la ruta es el elemento 1 de info_local
                        print(f'--El archivo {arch_local} se actualizo correctamente--')
                    elif fecha_remoto > fecha_local:
                        id_arch = archivos_remotos[arch_remoto][0]
                        os.remove(info_local[1])
                        descargar_archivo(id_arch)
                        print('lo descargamos al de arriba')
                        print(f'***El archivo {arch_local} no se actualizo ***')        
                        print(f'se descargo{id_arch}')
        else:                               #clave es el nombre

            ## SOLO DESCARGA ARCHIVOS 
            print(f'El archivo {arch_local} no se encuentra en el remoto')
            if arch_local != ".git" and arch_local != "__pycache__" :
                #recorrer_carpeta() --> esta llama a la otra q las crea

                subir_archivos(arch_local, info_local[1], carpeta_id)


def modificar_dic_arch_remoto(archivos_remotos):
    """
    PRE:
    
    POST:
    No devuelve nada. Modufico por referencia el dict "archivos_locales"
    con las sig estructura arch_remotos = { nombre_arch: [id_carpeta, fecha_modif] }
    """
    for archivo_remoto, info_archivo in archivos_remotos.items():
        
        #Modifico la fecha del remoto xa poderla comparar con la local (tambien hasta seg inclusive)
        nueva_fecha_remoto = info_archivo[1][:18].replace('T',' ')          #por error
        archivos_remotos[archivo_remoto][1] = nueva_fecha_remoto


def cargar_dic_arch_local(archivos_locales, ruta_actual):
    """
    PRE:
    POST: No devuelve nada. Modufico por referencia el dict "archivos_locales"
    con las sig estructura arch_locales = { nombre_arch: [modifiedTime, ruta_local] }
    """
    #for arch in list(pathlib.Path().glob('**/*')):  #recorro todooo
    # contenido = os.listdir(ruta_actual)
    # for ficheros in contenido :    
    with os.scandir(ruta_actual) as ficheros:
        for fichero in ficheros:
            if os.path.isfile(fichero):
                #obtengo hora de modif de cada archivo usando el objeto datetime
                hora_local = datetime.datetime.fromtimestamp(fichero.stat().st_mtime)
                
                #Sumo + 3 HORAS a hora LOCAL usando el objeto datetime
                horas = 3
                horas_sumadas = datetime.timedelta(hours = horas)
                nueva_hora_local = hora_local + horas_sumadas # sumo 3 horas

                #Convierto el objeto datetime en str
                fecha_local = str(nueva_hora_local)
                #le rcorto hasta los segundos inclusive por un tema de error
                fecha_local = fecha_local[:18]  
                
                #uso como clave el nombre del arch, y como valor una lista la fecha de mofi y la 
                # ruta
                archivos_locales[str(fichero.name)] = [fecha_local, fichero]


def sincronizar(id_carpeta, ruta_actual):
    """
    PRE: Recibe el dict/ list "" con los nombres de los archivos de la carpeta 
    q se esta sincronizando
    POST: No devuelve nada. Actualiza los archivos de la nube, reemplanzadolos por los locales.
    OJO!
    1 - las fechas de modif se aproximaron a los minutos por lo que si se modifica dentro del 
    #mismo minuto y se sincroiza no se matienen los cambios. OJO, una vez cometido el error,
    es necesario, esperar 1 minuto, modificar, actualizar. y recien 1 min dsps no se actualizara 
    mas.
    """
    
    #arch_locales = { nombre_arch: [modifiedTime, ruta_local] }
    archivos_locales = dict()
    
    cargar_dic_arch_local(archivos_locales, ruta_actual)
    
    #Traigo archivos de drive y cargo el diccionario archivos_remotos
    #arch_remotos = { nombre_arch: [id_carpeta, fecha_modif] }
    query = f"'{id_carpeta}' in parents and not trashed"   #esto es un win win porque solo archivos, ninguna carpeta
    carpetas_remotas, archivos_remotos = listar_elementos(query)
    
    #Modifico en el dict archivos_remotos la "modifiedTime" por referencia de
    #xa q coincida con la local
    modificar_dic_arch_remoto(archivos_remotos)
    modificar_dic_arch_remoto(carpetas_remotas)

    print(carpetas_remotas.keys())
    print(archivos_remotos.keys())


    push_local_a_remoto(archivos_locales, archivos_remotos,id_carpeta)

    #Sync remoto con local (modifico remoto)
    # print('1-Push (Modifica remoto, con cambios locales)\n2-pull(modifica local con cambios remotos')
    # opc = int(validar_opcion(1,2))
    # if opc == 1:
    #     push_local_a_remoto(archivos_locales, archivos_remotos,id_carpeta)
    # # else:
    #     pull_remoto_a_local(archivos_locales, archivos_remotos)

import os


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


# ruta_actual = os.getcwd()
# nombre_carpeta = ruta_actual.split("\\")[-1]
# id_carpeta = encontrar_carpeta_upstream(nombre_carpeta)[0]

#sincronizar(id_carpeta, ruta_actual)




####----------------------------------------------------

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

'''
import pickle
import hashlib #instead of md5

try:
    l = pickle.load(open("db"))
except IOError:
    l = []
db = dict(l)
path = "/etc/hosts"
#this converts the hash to text
checksum = hashlib.md5(open(path).read()).hexdigest() 
if db.get(path, None) != checksum:
    print ("file changed")
    db[path] = checksum
pickle.dump(db.items(), open("db", "w"))
'''