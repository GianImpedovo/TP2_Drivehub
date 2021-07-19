##import main
import os
import csv

RUTA = os.getcwd()



# Necesito recibir las evaluaciones de los alumnos por gmail
# para poder adjuntar cada examen a su carpeta  ---> []

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

# ----------- recorrido de carpetas 

def mostrar_directorio_actual(ruta_actual: str)->None:
    '''
    PRE: Recibo la ruta donde me encuntro
    POST: Retorno un listado de los elementos que se encuentran en donde estoy parado
    '''
    print(ruta_actual)
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

def recorrer_directorio(ruta_actual: str)->None:
    mostrar_directorio_actual(ruta_actual)
    print(ruta_actual)
    for dirpath, dirnames, filenames in os.walk(ruta_actual):
        ", ".join(dirnames)
        ", ".join(filenames)

        print("\n ---> Recorrer directorio , si desea salir escriba 'salir'")
        accion = input("A que directorio/archivo desea ir: ")
        if accion == "salir":
            ruta_actual = "/home/gianfranco/Documentos/fiuba/Algoritmos/TP2" # cambiar por la ruta del usuario
            break # me lleva al main
        elif accion == "mover":
            if os.path.isdir(ruta_actual):
                recorrer_directorio(ruta_actual + "/" + accion)
            else:
                pass
                # abrir el archivo


recorrer_directorio(RUTA)