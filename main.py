
import os
import service_drive
import service_gmail
from pathlib import Path
import csv

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from zipfile import ZipFile
import shutil
from zipfile import ZipFile
import pprint

import funcionalidad_drive as drive

RUTA = os.getcwd()

MENU = ["COMANDOS : 'cd + < nombre_directorio >' (avanzo directorio), '..' (retrocedo)",
        "1 - Listar archivos de la carpeta actual",
        "2 - Crear archivos",
        "3 - Subir archivos",
        "4 - Descargar un archivo",
        "5 - Sincronizar",
        "6 - Generar carpeta de una evaluacion",
        "7 - Actualizar entregas de alumnos via mail",
        "8 - Salir"
        ]

def mostrar_menu(ruta: str)->None:
    print()
    for x in MENU:
        print(x)
    print("RUTA ACTUAL : " ,ruta)
    print("\nElija una opcion: ")

## --------------- RECORRER TODO --------------------------------------------------------------
def mostrar_directorio_actual(ruta_actual: str)->None:
    '''
    PRE: Recibo la ruta donde me encuntro
    POST: Retorno un listado de los elementos que se encuentran en donde estoy parado
    '''
    print("\n - CARPETA ACTUAL (LOCAL)-")
    print("--> DIRECTORIO : ",ruta_actual)
    contenido = os.listdir(ruta_actual)
    for fichero in contenido:
        if os.path.isfile(ruta_actual + "/" + fichero):
            print("Archivo - ",fichero)
        else:
            print("Carpeta - ",fichero)
            contenido_carpeta = os.listdir(ruta_actual + "/" + fichero)

            for contenido in contenido_carpeta:
                if os.path.isdir(ruta_actual + "/" + fichero + "/" + contenido):
                    print(" -> carpeta: ", contenido)
                else:
                    print(" -> archivo:  ",contenido)

def recorrer_directorio(ruta_actual: str, comando: str)->None:
    '''
    PRE: recibe la ubicacion donde me encuentro 
    POST: Puedo recorrer los ficheros
    '''
    for dirpath, dirnames, filenames in os.walk(ruta_actual):
        ", ".join(dirnames)
        ", ".join(filenames)

        if "cd" == comando[0]:
            if os.path.isdir(ruta_actual + "/" + comando[1]):
                ruta_actual = (ruta_actual + "/" + comando[1])
            else:
                print(f"\t --- La carpeta: '{comando[1]}' NO existe --- \t")
        elif ".." == comando[0]:
            print("\n",ruta_actual)
            actual = ruta_actual.split("/")
            actual.pop(-1)
            actual = "/".join(actual)
            print(actual)
            ruta_actual = actual

        return ruta_actual

def directorio_actual(ruta: str)->str:
    ruta_actual = ruta
    ruta = ruta.split("/")
    directorio_actual = ruta[-1]
    return ruta_actual, directorio_actual

# ---------------- CREAR CARPETA/ARCHIVO ------------------(CODIGO ANTO)
# -------> Carpetas
def crear_carpetas(nombre: str, ruta: str)->None:
    os.mkdir(ruta + "/" + nombre)
    print(f"Carpeta: {nombre} fue creada con exito")

# -------> Archivos
def crear_txt(nombre: str, ruta : str)->None:
    file = open(ruta + "/" + nombre, "w")
    file.close()
    print(f"Archivo: {nombre} fue creada con exito")

def crear_csv():
    nombre = input('Ingrese nombre para crear archivo .csv: ')
    with open(nombre+'.csv', 'w', newline='') as csvfile:
        salir = 0
        fieldnames = []
        while salir != 1:
            fieldnames.append(input('Ingrese nombre de la columna: '))
            salir = int(input('Ingrese 1 para terminar casillas, 2-9 para agregar otra: '))
        
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        salir = False
        while not salir :
            datos={}      
            for i in range(len(fieldnames)):
                datos[fieldnames[i]] = input('Ingrese el valor de la casilla '+ fieldnames[i] + ': ')   
            writer.writerow(datos)
            salir = input("Desea seguir agregando filas al archivo (s/n): ")
            if salir != "s": salir = True
            else : salir = False

def modificar_csv(archivo: str):
    
    with open(archivo) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        dict_from_csv = dict(list(csv_reader)[0])
        list_of_column_names = list(dict_from_csv.keys())

    with open(archivo, "a", newline='') as csvfile:
        writer = csv.DictWriter(csvfile,delimiter=',', fieldnames = list_of_column_names[0])
        
        salir = False
        while not salir:
            datos={}
            for i in range(len(list_of_column_names[0])):
                datos[list_of_column_names[0][i]] = input('Ingrese el valor de la casilla '+ list_of_column_names[0][i]+ ': ')
            writer.writerow(datos)
            salir = input("Desea seguir agregando (s/n): ")
            if salir != "s": salir = True
            else : salir = False

def crear_archivos(elegir: str, ruta: str)->None:
    if elegir == '1':
        nombre = input('Ingrese un nombre para el archivo .txt: ')
        crear_txt(nombre+'.txt', ruta)
        
    elif elegir == '2':
        crear_csv()
    
    elif elegir == '3':
        print("\nIngrese el nombre del archivo con su extension ej: alumnos.csv")
        nombre_archivo = input("Archivo: ")
        modificar_csv(nombre_archivo)

    elif elegir == '4':
        nombre = input('Ingrese nombre para la carpeta: ')
        crear_carpetas(nombre, ruta)

# -------> Matcheo archivo docentes , alumnos:
def crea_csv_DA(diccionario_alumno_docente: dict(), nombre_del_archivo: str)->None:
    '''
    PRE: Recibe el diccionario con la relacion docente alumno
    POST: Crea el archivo csv con dicha
    '''
    ''' asumo que el archivo no existe '''
    with open(nombre_del_archivo, 'w') as archivo:
        csv_writer = csv.writer(archivo, delimiter = ',')
        csv_writer.writerow(["Docente","Alumno"])

        for profesor , alumnos in diccionario_alumno_docente.items():
            for alumno in alumnos:
                csv_writer.writerow((profesor, alumno))
    print("\n ### Se creo con exito el archivo que relaciona los docentes y los alumnos ### ")

def crea_relacion_DA(lista_alumnos: list(),lista_docentes: list(),nombre_archivo: str)->None:
    '''
    PRE: Recibe las listas creadas de los docentes y los alumnos
    POST: Crea un diccionario con la relacion clave: docente, valor: lista de alumnos
    '''
    diccionario_alumno_docente = dict()
    while len(lista_alumnos) != 0:
        for profesor in range(len(lista_docentes)):
            if len(lista_alumnos) != 0:
                alumno = lista_alumnos.pop(0)
                if lista_docentes[profesor] in diccionario_alumno_docente:
                    diccionario_alumno_docente[lista_docentes[profesor]].append(alumno)
                else:
                    diccionario_alumno_docente[lista_docentes[profesor]] = [alumno]
    
    crea_csv_DA(diccionario_alumno_docente,nombre_archivo)

def crear_archivo_alumnos_docentes(archivo_alumnos: str, archivo_docentes: str, nombre_archivo: str)->None:
    '''
    PRE: Recibe los archivos a matchear
    POST: En caso que los archivos existan los envia a la funcion para que los relacione
    '''
    try : 
        lista_alumnos = list()
        lista_docentes = list()
        with open(archivo_alumnos) as alumnos:
            for linea in alumnos:
                linea = linea.strip().split(",")
                if linea[0] != "Nombre":
                    lista_alumnos.append(linea[0])
        with open(archivo_docentes) as docentes:
            for linea in docentes:
                linea = linea.strip().split(",")
                if linea[0] != "Nombre":
                    lista_docentes.append(linea[0])
        crea_relacion_DA(lista_alumnos,lista_docentes,nombre_archivo)
    except:
        print("\nUno de estos archivos NO existe.")

def diccionario_docentes(archivo_docente_alumno: str)->dict:
    '''
    PRE: Recibe csv relacion de docentes y alumnos
    POST: Retorna un diccionario con esta relacion
    '''
    dict_docentes = dict()
    with open(archivo_docente_alumno, newline='', encoding="UTF-8") as archivo:

        csv_reader = csv.reader(archivo, delimiter=',')
        next(csv_reader)

        for linea in archivo:
            linea = linea.strip().split(",")
            if linea[0] in dict_docentes:
                dict_docentes[linea[0]].append(linea[1])
            else:
                dict_docentes[linea[0]] = [linea[1]]
    
    return dict_docentes


# ---------------- CREAR CARPETA DE EVALUACION (LOCAL)------------------
# ---> envio mail de instrucciones :
INSTRUCCIONES = "crear carpeta evaluacion\ncrear otras carpetas"

def enviar_email_instrucciones(email: str)->None:
    '''
    PRE: Recibe el mail del docente que desea crear una carpeta de evaluacion
    POST: Envia mail al docente con las instrucciones
    '''
    servicio = service_gmail.obtener_servicio()
    msj = INSTRUCCIONES
    mime_mensaje = MIMEMultipart()
    mime_mensaje['subject'] = 'Instrucciones para crear carpeta Evaluacion'
    mime_mensaje['to'] = email
    mime_mensaje.attach(MIMEText(msj, 'plain'))
    raw_string = base64.urlsafe_b64encode(mime_mensaje.as_bytes()).decode()
    mensaje = servicio.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print(mensaje) 

def crear_carpeta_sobrantes(directorio_evaluacion: str)->None:
    '''
    PRE: Recibo el directorio donde estan las evaluaciones
    POST: Para los alumnos no matcheados se les crea una carpeta aparte donde seran guardados sus examenes
    '''
    os.mkdir(directorio_evaluacion + "/" + "sobrantes")
    alumnos_sobrantes = directorio_evaluacion + "/" + "sobrantes" + "/"
    ruta_alumnos_sobrantes = os.getcwd() + "/" + "evaluacion" + "/"
    lista_sobrantes = os.listdir(ruta_alumnos_sobrantes)
    for sobrante in lista_sobrantes:
        ruta_alumnos_sobrantes += sobrante
        shutil.move(ruta_alumnos_sobrantes, alumnos_sobrantes)

def crear_carpeta_alumnos(dict_docentes: dict(),directorio_evaluacion: str, profesor: str)->None:
    '''
    PRE: recibe la relacion de los docentes y sus alumnos
    POST: dentro de la carpeta del profesor correspondiente crea la carpeta de los alumnos que debe corregir
    '''
    
    lista_alumnos = dict_docentes[profesor]
    for alumno in lista_alumnos:
        ruta_alumno = directorio_evaluacion + "/" + profesor + "/"
        ruta_evaluaciones = os.getcwd() + "/" + "evaluacion" + "/" + alumno + "/"
        if os.path.isdir(ruta_evaluaciones):
            shutil.move(ruta_evaluaciones, ruta_alumno)
    
    # ingresar en cada carpeta del alumno su examen []

def crear_carpeta_profesores(archivo_docente_alumno: str, ruta_ev: str)->None:
    '''
    PRE: recibe los archivos correspondientes 
    POST: crea las carpetas de los docentes dentro de la evaluacion 
    '''
    dict_docentes = diccionario_docentes(archivo_docente_alumno)

    directorio_evaluacion = ruta_ev
    for profesor in dict_docentes.keys():
        os.mkdir(directorio_evaluacion + "/" + profesor)

        crear_carpeta_alumnos(dict_docentes,directorio_evaluacion, profesor)

    crear_carpeta_sobrantes(directorio_evaluacion)
    shutil.rmtree(os.getcwd() + "/" + "evaluacion")

def crear_carpeta_evaluacion(ruta: str)->None: 
    '''
    PRE: Recibe la ruta de la ubicacion donde se encuentra el usuario
    POST: usando las distintas funciones para anidar crea la carpeta de la evaluacion
    '''
    nombre_ev = input("Nombre de la evalucaion: ")
    archivo_alumnos = "alumnos.csv"
    archivo_docentes = "docentes.csv"
    archivo_docente_alumno = "relacion"

    nombre_csv_DA = archivo_docente_alumno + ".csv"
    crear_archivo_alumnos_docentes(archivo_alumnos, archivo_docentes,nombre_csv_DA)

    ruta_ev = ruta + "/" + nombre_ev
    os.mkdir(ruta_ev)

    os.getcwd()
    
    crear_carpeta_profesores(nombre_csv_DA, ruta_ev)

# --------------------- RECEPCION DE EVALUACIONES ---------- (CODIGO ADO)
def obtener_email(id_mensaje):
    servicio = service_gmail.obtener_servicio()
    mensaje = servicio.users().messages().get(userId='me',id=id_mensaje).execute()
    return mensaje

def obtener_lista_email():
    servicio = service_gmail.obtener_servicio()
    resultados = servicio.users().messages().list(userId='me', q='in:inbox', maxResults=1).execute()
    #resultados = servicio.users().messages().list(userId='me', q='in:inbox is:unread', maxResults=1).execute()
    #pprint.pprint(resultados)
    return resultados.get('messages',[])

def enviar_email(email):
    servicio = service_gmail.obtener_servicio()
    msj = 'ENTREGA OK'
    mime_mensaje = MIMEMultipart()
    mime_mensaje['subject'] = 'EVALUACION'
    mime_mensaje['to'] = email
    mime_mensaje.attach(MIMEText(msj, 'plain'))
    raw_string = base64.urlsafe_b64encode(mime_mensaje.as_bytes()).decode()
    mensaje = servicio.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print(mensaje)    

def descomprimir_archivo(name):

    archivo = "./evaluaciones_zip/"+name+".zip"

    #with ZipFile(archivo, 'r') as zip:
    #    zip.printdir()
    #    zip.extractall() 
    #print("Archivo desconprimido.")

    with ZipFile(archivo, 'r') as evaluacion:
        nombres_archivo = evaluacion.namelist()
        for nombre_archivo in nombres_archivo: 
            if nombre_archivo.endswith('.py'):
                evaluacion.extract(nombre_archivo, 'evaluaciones_zip/'+name)
                print("Archivo desconprimido.")

def obtener_evaluaciones():
    mensajes = obtener_lista_email()
    email = ''
    titulo = ''
    for msj in mensajes:
        #print(msj['id'])
        #pprint.pprint(msj)
        #pprint.pprint(obtener_email(msj['id']))
        msj_detalles = obtener_email(msj['id'])
        pprint.pprint(msj_detalles)
        msj_detalles = msj_detalles["payload"]["headers"]

        for msj_detalle in msj_detalles: 

            if msj_detalle["name"] == 'To':
                email = msj_detalle["value"]
                print("email",email)
            if msj_detalle["name"] == 'Subject':   
                titulo = msj_detalle["value"]
                print("titulo",titulo)
        #descomprimir_archivo(titulo)    
        #enviar_email(email)

def validar_entrega(name):
    print("validar")

#if __name__ == '__main__':
#enviar_email('adrodriguez@fi.uba.ar')
#descomprimir_archivo("108367 - Rodriguez, Adonis")
#obtener_evaluaciones()

# ------------------------------ DRIVE 

def main()-> None:
    ruta_actual = RUTA
    mostrar_menu(ruta_actual)
    opcion = input("opcion : ")

    while (opcion[0] != "8"):
        opcion = opcion.split(" ")
        # --------  Navegacion :
        if opcion[0] == "cd" or opcion[0] == "..":
            comando = opcion
            ruta_actual = recorrer_directorio(ruta_actual, comando)

        # Acciones para realizar dentro del directorio: 
        elif opcion[0] == "1":
            elegir = input("1 - Local\n2 - Remoto\n -> ")
            if elegir == "1":
                mostrar_directorio_actual(ruta_actual)
            elif elegir == "2":
                drive.consultar_elementos()

        elif opcion[0] == "2":
            
            print('\n1 - Archivo .txt\n2 - Archivo .csv\n3 - Modificar .csv\n4 - Carpeta\n5 - salir')
            ## fijar salir []
            print('Elija una opcion:\n')
            eleccion = input('Opcion: ')
            crear_archivos(eleccion, ruta_actual)
            ## -> subir el archivo creado
            if eleccion == "4":
                print(" ------ Navega por tu drive y crea la carpeta donde quiera !  ------ ")
                print("\nIngrese el nombre de la carpeta creada recientemente")
                nombre_carpeta = input(" -> ")
                print("\n Eliga la ubicacion donde quiera crear la carpeta en el remoto")
                id_elemento = drive.consultar_elementos()[0]
                drive.crea_carpetas(nombre_carpeta,id_elemento)
                
            else :
                ## subo el archivo a drive
                print("\n --- Suba el archivo recien creado a su drive ---  ")
                print("Ingrese el nombre del archivo recien creado con la extension -> ej: texto.txt")
                nombre_archivo = input("Archivo: ")
                ruta_archivo = RUTA + "/" + nombre_archivo
                carpeta_contenedora = ruta_actual.split("/")[-1]
                drive.opciones_subir_archivos(nombre_archivo, ruta_archivo, carpeta_contenedora)

        elif opcion[0] == "3":
            elegir = input("\n1 - Subir archivo\n2 - Subir carpeta\n -> ")
            if elegir == "1":
                print(" ------ Navega por tu drive y subi el archivo a donde quieras !  ------ ")
                nombre_archivo = input("Ingrese el nombre del archivo que quiera subir : ")
                ruta_actual = RUTA + "/" + nombre_archivo
                carpeta = RUTA.split("/")[-1]
                drive.menu_subir_archivos(ruta_actual, nombre_archivo, carpeta)
            elif elegir == "2":
                carpeta_a_descargar = input("Ingrese el nombre de la carpeta que desea descargar\n -> ")
                ruta = os.getcwd() + "/" + carpeta_a_descargar
                drive.recorrer_carpeta(ruta)

        elif opcion[0] == "4":
            drive.menu_descargar_elementos(ruta_actual)

        elif opcion[0] == "5":
            directorio_actual = RUTA.split("/")[-1]
            print(f"\n Sincroniza {directorio_actual}")
            sincronizacion = input(f"Desea sincronizar la carpeta {directorio_actual} (s/n): ")
            if sincronizacion == "s":
                carpeta_id = drive.encontrar_carpeta_upstream(directorio_actual)[0]
                drive.sincronizar(carpeta_id)
                ## drive.sincronizar()
                pass
            ## sincronizar la carpeta en donde estoy parado
            pass

        elif opcion[0] == "6":
            email_usuario = input("Introduzca su email para enviarle las instrucciones: ")
            enviar_email_instrucciones(email_usuario)

        elif opcion[0] == "7":
            crear_carpeta_evaluacion(ruta_actual)

        mostrar_menu(ruta_actual)
        opcion = input("opcion : ")

main()
