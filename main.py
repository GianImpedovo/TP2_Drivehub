
import os
import service_drive
import service_gmail


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
