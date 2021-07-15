##import main
import os
import csv

RUTA = os.getcwd()
print(RUTA)


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

crear_carpeta_evaluacion()