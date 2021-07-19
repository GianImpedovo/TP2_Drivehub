
import os
import service_drive
import service_gmail
from pathlib import Path
import csv

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
    print("\n - CARPETA ACTUAL -")
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

# ---------------- CREAR CARPETA/ARCHIVO ------------------
# -------> Carpetas
def crear_carpetas(nombre: str, ruta: str)->None:
    os.mkdir(ruta + "/" + nombre)
    print(f"Carpeta: {nombre} fue creada con exito")

# -------> Archivos
def crear_txt_csv(nombre: str, ruta : str)->None:
    file = open(ruta + "/" + nombre, "w")
    file.close()
    print(f"Archivo: {nombre} fue creada con exito")

def crear_archivos(elegir: str, ruta: str)->None:
    if elegir == '1':
        nombre = input('Ingrese un nombre para el archivo .txt: ')
        crear_txt_csv(nombre+'.txt', ruta)
        
    elif elegir == '2':
        nombre = input('Ingrese un nombre para el archivo .csv: ')
        crear_txt_csv(nombre+'.csv', ruta)

    elif elegir == '3':
        nombre = input('Ingrese nombre para la carpeta: ')
        crear_carpetas(nombre, ruta)

# -------> Matcheo archivo docentes , alumnos:
def crea_csv_DA(diccionario_alumno_docente, nombre_del_archivo):
    ''' asumo que el archivo no existe '''
    with open(nombre_del_archivo, 'w') as archivo:
        csv_writer = csv.writer(archivo, delimiter = ',')
        csv_writer.writerow(["Docente","Alumno"])

        for profesor , alumnos in diccionario_alumno_docente.items():
            for alumno in alumnos:
                csv_writer.writerow((profesor, alumno))
    print("\n ### Se creo con exito el archivo que relaciona los docentes y los alumnos ### ")

def crea_relacion_DA(lista_alumnos,lista_docentes,nombre_archivo):
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

def crear_archivo_alumnos_docentes(archivo_alumnos, archivo_docentes, nombre_archivo):
    lista_alumnos = list()

    lista_docentes = list()
    with open(archivo_alumnos) as alumnos:
        for linea in alumnos:
            linea = linea.strip().split(",")
            lista_alumnos.append(linea[0])
    with open(archivo_docentes) as docentes:
        for linea in docentes:
            linea = linea.strip().split(",")
            lista_docentes.append(linea[0])

    print(lista_docentes)
    print(lista_alumnos)

    crea_relacion_DA(lista_alumnos,lista_docentes,nombre_archivo)

# ---------------- CREAR CARPETA DE EVALUACION (LOCAL)------------------
def crear_carpeta_alumnos(dict_docentes,directorio_evaluacion, profesor):
    lista_alumnos = dict_docentes[profesor]
    for alumno in lista_alumnos:
        os.mkdir(directorio_evaluacion + "/" + profesor + "/" + alumno)
    
    # ingresar en cada carpeta del alumno su examen []

def crear_carpeta_profesores(archivo_docente_alumno, ruta_ev):
    dict_docentes = dict()
    with open(archivo_docente_alumno, newline='', encoding="UTF-8") as archivo:

        csv_reader = csv.reader(archivo_docente_alumno, delimiter=',')
        next(csv_reader)

        for linea in archivo:
            linea = linea.strip().split(",")
            if linea[0] in dict_docentes:
                dict_docentes[linea[0]].append(linea[1])
            else:
                dict_docentes[linea[0]] = [linea[1]]

    directorio_evaluacion = ruta_ev
    dict_docentes.pop("Docente")

    for k in dict_docentes.keys():
        os.mkdir(directorio_evaluacion + "/" + k)

        crear_carpeta_alumnos(dict_docentes,directorio_evaluacion, k)

## Necesito recibir los archivos csv 
## y mas que nada una funcion que relacion a los alumnos con los profesores ---> []

def crear_carpeta_evaluacion(ruta): 
    nombre_ev = input("Nombre de la evalucaion: ")
    archivo_alumnos = input("ingrese el nombre del archivo de los alumnos cursando: ")
    archivo_docentes = input("ingrese el nombre del archivo de los docentes:")
    archivo_docente_alumno = input("nombre que le quiere poner al nuevo archivo de docentes y alumnos: ")

    
    nombre_csv_DA = archivo_docente_alumno + ".csv"
    crear_archivo_alumnos_docentes(archivo_alumnos, archivo_docentes,nombre_csv_DA)

    ruta_ev = ruta + "/" + nombre_ev
    os.mkdir(ruta_ev)

    os.getcwd()

    crear_carpeta_profesores(nombre_csv_DA, ruta_ev)


def main()-> None:
    ruta_actual = RUTA
    mostrar_menu(ruta_actual)
    opcion = input("opcione : ")

    while opcion != "8":
        opcion = opcion.split(" ")
        # --------  Navegacion :
        if opcion[0] == "cd" or opcion[0] == "..":
            comando = opcion
            ruta_actual = recorrer_directorio(ruta_actual, comando)

        # Acciones para realizar dentro del directorio: 
        elif opcion[0] == "1":
            mostrar_directorio_actual(ruta_actual)
            ## FALTA MOSTRAR EL DIRECTORIO REMOTO []

        elif opcion[0] == "2":
            print('\n1 - Archivo .txt\n2 - Archivo .csv\n3 - Carpeta\n')
            print('Elija una opcion:\n')
            elegir = input('Opcion: ')
            crear_archivos(elegir, ruta_actual)
            ## FALTA PODER CREAR ARCHIVOS EN DRIVE []

        elif opcion[0] == "3":
            ## FALTA PODER SUBIR (DE LOCAL A REMOTO) ARCHIVO []
            pass
        elif opcion[0] == "4":
            ## FALTA PODER DESCARGAR (DE REMOTO A LOCAL) ARCHIVO []
            pass
        elif opcion[0] == "5":
            ## FALTA PODER SINCRONIZAR , FUN_DRIVE []
            pass
        elif opcion[0] == "6":
            ## FALTA ENVIAR MAIL CON ESPECIFICACIONES PARA CREAR CARPETA DE EVALUACIONES []
            
            # enviar_mail()
            # una vez enviado el mail: 
            crear_carpeta_evaluacion(ruta_actual)
            pass
        elif opcion[0] == "7":
            pass
        elif opcion[0] == "8":
            pass
        
        mostrar_menu(ruta_actual)
        opcion = input("opcion : ")

main()
