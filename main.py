
import os
import service_drive
import service_gmail
from pathlib import Path

RUTA = os.getcwd()

MENU = ["1 - Listar archivos de la carpeta actual",
        "2 - Crear archivos",
        "3 - Subir archivos",
        "4 - Descargar un archivo",
        "5 - Sincronizar",
        "6 - Generar carpeta de una evaluacion",
        "7 - Actualizar entregas de alumnos via mail",
        "8 - Salir"
        ]

def mostrar_menu()->None:
    print()
    for x in MENU:
        print(x)
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

def recorrer_directorio(ruta_actual: str )->None:
    '''
    PRE: recibe la ubicacion donde me encuentro 
    POST: Puedo recorrer los ficheros
    '''

    print("\n ---> Recorrer directorio : 'cd' : moverse entre directorios ; 'salir' ; '..' retrocede")
    
    mostrar_directorio_actual(ruta_actual)
    
    for dirpath, dirnames, filenames in os.walk(ruta_actual):
        ", ".join(dirnames)
        ", ".join(filenames)
        print("\n",ruta_actual)
        accion = input("Accion que desea realizar: ").split()
        print(accion)
        while accion[0] != "salir":
            if "cd" == accion[0]:
                print("\n",ruta_actual)
                if os.path.isdir(ruta_actual):
                    recorrer_directorio(ruta_actual + "/" + accion[1])
                else:
                    pass
                    # abrir el archivo
            elif ".." == accion[0]:
                print("\n",ruta_actual)
                actual = ruta_actual.split("/")
                actual.pop(-1)
                actual = "/".join(actual)
                recorrer_directorio(actual)

def directorio_actual(ruta: str)->str:
    ruta_actual = ruta
    ruta = ruta.split("/")
    directorio_actual = ruta[-1]
    return ruta_actual, directorio_actual

# directorio_actual(RUTA)
# recorrer_directorio(RUTA)
## --------------------------------------------------------------------------------------------

# ---------------- CREAR CARPETA DE EVALUACION ------------------
def crear_carpeta_alumnos(dict_docentes,directorio_evaluacion, profesor):
    lista_alumnos = dict_docentes[profesor]
    for alumno in lista_alumnos:
        os.mkdir(directorio_evaluacion + "/" + profesor + "/" + alumno)
    
    # ingresar en cada carpeta del alumno su examen []

def crear_carpeta_profesores(archivo_docente_alumno, nombre_ev):
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

    directorio_evaluacion = RUTA + "/" + nombre_ev
    dict_docentes.pop("Docente")

    for k in dict_docentes.keys():
        os.mkdir(directorio_evaluacion + "/" + k)

        crear_carpeta_alumnos(dict_docentes,directorio_evaluacion, k)

## Necesito recibir los archivos csv 
## y mas que nada una funcion que relacion a los alumnos con los profesores ---> []

def crear_carpeta_evaluacion(): 
    nombre_ev = input("Nombre de la evalucaion: ")
    archivo_alumnos = input("ingrese el nombre del archivo de los alumnos cursando: ")
    archivo_docentes = input("ingrese el nombre del archivo de los docentes:")
    archivo_docente_alumno = "d_a.csv" # cambiar por la funcion que trar los archivos matcheados []

    os.mkdir(nombre_ev)

    os.getcwd()

    crear_carpeta_profesores(archivo_docente_alumno, nombre_ev)

#crear_carpeta_evaluacion()
## --------------------------------------------------------------------------------------------

# ---------------- CREAR CARPETA/ARCHIVO ------------------
# -------> Carpetas
def crear_carpetas(nombre: str):
    Path(nombre).mkdir(exist_ok=True)

def crear_carpeta_sobre_carpeta(nombre1: str, nombre2: str, nombre3: str):
    os.makedirs(os.path.join(nombre1, nombre2, nombre3))

# -------> Archivos
def crear_txt_csv(nombre: str):
    file = open(nombre, "w")

def crear_archivos(elegir: str):
    if elegir == '1':
        nombre = input('Ingrese un nombre para el archivo .txt: ')
        crear_txt_csv(nombre+'.txt')
        
    elif elegir == '2':
        nombre = input('Ingrese un nombre para el archivo .csv: ')
        crear_txt_csv(nombre+'.csv')

    elif elegir == '3':
        opcion = input('Ingrese:\n[1]Para crear una carpeta\n[2]Crear carpetas multiples\n')
        if opcion == '1':
            nombre = input('Ingrese nombre para la carpeta: ')
            crear_carpetas(nombre)
        elif opcion == '2':
            nombre1 = input('Ingrese un nombre para la carpeta : ')
            nombre2 = input('Ingrese un nombre para la carpeta : ')
            nombre3 = input('Ingrese un nombre para la carpeta : ')
            crear_carpeta_sobre_carpeta(nombre1, nombre2, nombre3)

# -------> Matcheo archivo docentes , alumnos:
def crea_csv_DA(diccionario_alumno_docente):
    ''' asumo que el archivo no existe '''
    with open("d_a.csv", 'w') as archivo:
        csv_writer = csv.writer(archivo, delimiter = ',')
        csv_writer.writerow(["Docente","Alumno"])

        for profesor , alumnos in diccionario_alumno_docente.items():
            for alumno in alumnos:
                csv_writer.writerow((profesor, alumno))

def crea_relacion_DA(lista_alumnos,lista_docentes):
    diccionario_alumno_docente = dict()
    while len(lista_alumnos) != 0:
        for profesor in range(len(lista_docentes)):
            alumno = lista_alumnos.pop(0)
            if lista_docentes[profesor] in diccionario_alumno_docente:
                diccionario_alumno_docente[lista_docentes[profesor]].append(alumno)
            else:
                diccionario_alumno_docente[lista_docentes[profesor]] = [alumno]
    
    crea_csv_DA(diccionario_alumno_docente)


def crear_archivo_alumnos_docentes(archivo_alumnos, archivo_docentes):
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

    crea_relacion_DA(lista_alumnos,lista_docentes)

# crear_archivo_alumnos_docentes("alumnos.csv", "docentes.csv")
'''
def main()-> None:
    
    mostrar_menu()
    opcion = input("opcione : ")
    while opcion != "8":
        
        if opcion == "1":
            pass
        elif opcion == "2":
            pass
        elif opcion == "3":
            pass
        elif opcion == "4":
            pass
        elif opcion == "5":
            pass
        elif opcion == "6":
            pass
        elif opcion == "7":
            pass
        elif opcion == "8":
            pass
        
        mostrar_menu()
        opcion = input("opcion : ")
    
main()
'''
