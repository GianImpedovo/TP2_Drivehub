##import main
import shutil,os
import csv

RUTA = os.getcwd()
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


# ---> creo la carpeta evaluacion 
def crear_carpeta_sobrantes(directorio_evaluacion):
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
        os.mkdir(directorio_evaluacion + "/" + profesor + "/" + alumno)
        ruta_alumno = directorio_evaluacion + "/" + profesor + "/" + alumno
        ruta_evaluaciones = os.getcwd() + "/" + "evaluacion" + "/" + alumno + "/"
        if os.path.isdir(ruta_evaluaciones):
            shutil.move(ruta_evaluaciones, ruta_alumno)
    
    # ingresar en cada carpeta del alumno su examen []

def crear_carpeta_profesores(archivo_docente_alumno: str, ruta_ev: str)->None:
    '''
    PRE: recibe los archivos correspondientes 
    POST: crea las carpetas de los docentes dentro de la evaluacion 
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

    directorio_evaluacion = ruta_ev
    for k in dict_docentes.keys():
        os.mkdir(directorio_evaluacion + "/" + k)

        crear_carpeta_alumnos(dict_docentes,directorio_evaluacion, k)

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

crear_carpeta_evaluacion(RUTA)

