
import os
import service_drive
import service_gmail


import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from zipfile import ZipFile
import shutil
from zipfile import ZipFile
import pprint


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

main()
