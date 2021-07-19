import os
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


def listar_todos_archivos():
    for i in list(Path().iterdir()):
        print(i)
def crear_txt_csv(nombre: str):
    file = open(nombre, "w")

    
def crear_carpetas(nombre: str):
    Path(nombre).mkdir(exist_ok=True)

def crear_carpeta_sobre_carpeta(nombre1: str, nombre2: str, nombre3: str):
    os.makedirs(os.path.join(nombre1, nombre2, nombre3))

def mostrar_menu():
    print()
    for x in MENU:
        print(x)
    print("\nElija una opcion: ")
    
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
        

def main() -> None:
    mostrar_menu()
    opcion = input("opcione : ")
    while opcion != "8":

        if opcion == "1":
            listar_todos_archivos()
            
        elif opcion == "2":
            
            print('1 - Archivo .txt\n2 - Archivo .csv\n3 - Carpeta\n')
            print('Elija una opcion:\n')
            elegir = input('Opcion: ')
            crear_archivos(elegir)
            
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