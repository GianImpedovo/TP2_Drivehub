##import main
import os
import csv

RUTA = os.getcwd()
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

    crea_relacion_DA(lista_alumnos,lista_docentes,nombre_archivo)

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
    archivo_docente_alumno = input("nombre que le quiere poner al nuevo archivo de docentes y alumnos: ")

    
    nombre_csv_DA = archivo_docente_alumno + ".csv"
    crear_archivo_alumnos_docentes("alumnos.csv", "docentes.csv",nombre_csv_DA)
    os.mkdir(nombre_ev)

    os.getcwd()

    crear_carpeta_profesores(nombre_csv_DA, nombre_ev)

    return nombre_csv_DA

crear_carpeta_evaluacion()

