
import os
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
from datetime import datetime, date, time, timedelta
import mimetypes
from email.mime.base import MIMEBase
from email import encoders
from email.mime.application import MIMEApplication
import funcionalidad_drive as drive

RUTA = os.getcwd()

MENU = ["COMANDOS : 'cd + < nombre_directorio >' (avanzo directorio), '..' (retrocedo), 'mv.remoto' (mueve archivos desde el remoto)",
        "1 - Listar archivos de la carpeta actual",
        "2 - Crear archivos",
        "3 - Subir archivos",
        "4 - Descargar un archivo",
        "5 - Sincronizar",
        "6 - Generar carpeta de una evaluacion",
        "7 - Actualizar entregas de alumnos via mail",
        "8 - Salir"
        ]

SEP = drive.definir_sistema()

def mostrar_menu(ruta: str)->None:
    """
    PRE: Recibo la ruta actual
    POST: Imprime el menu y la ruta donde el usuario se encuentra
    """
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
        if os.path.isfile(ruta_actual + SEP + fichero):
            print("Archivo - ",fichero)
        else:
            print("Carpeta - ",fichero)
            contenido_carpeta = os.listdir(ruta_actual + SEP + fichero)

            for contenido in contenido_carpeta:
                if os.path.isdir(ruta_actual + SEP + fichero + SEP + contenido):
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
            if os.path.isdir(ruta_actual + SEP + comando[1]):
                ruta_actual = (ruta_actual + SEP + comando[1])
            else:
                print(f"\t --- La carpeta: '{comando[1]}' NO existe --- \t")
        elif ".." == comando[0]:
            print("\n",ruta_actual)
            actual = ruta_actual.split(SEP)
            actual.pop(-1)
            actual = SEP.join(actual)
            print(actual)
            ruta_actual = actual

        return ruta_actual

def directorio_actual(ruta: str)->str:
    """
    PRE: Recibe la ruta actual
    POST: Retorna el directorio y la ruta del directorio
    """
    ruta_actual = ruta
    ruta = ruta.split(SEP)
    directorio_actual = ruta[-1]
    return ruta_actual, directorio_actual

# ---------------- CREAR CARPETA/ARCHIVO ------------------(CODIGO ANTO)
# -------> Carpetas
def crear_carpetas(nombre: str, ruta: str)->None:
    """
    PRE : Ingresa el nombre de la carpeta nueva
    POST : Crea la carpeta 
    """
    os.mkdir(ruta + SEP + nombre)
    print(f"Carpeta: {nombre} fue creada con exito")

# -------> Archivos
def crear_txt(nombre: str, ruta : str)->None:
    """
    PRE: Recibe el nombre del nuevo archivo txt
    POST: Crea el archivo
    """
    file = open(ruta + SEP + nombre, "w")
    file.close()
    print(f"Archivo: {nombre} fue creada con exito")

def crear_csv()->None:
    """
    PRE: No recibe ningun parametro , todo se crea dentro de la funcion
    POST:  Crea un archivo csv
    """
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

def modificar_csv(archivo: str)->None:
    """
    PRE: Recibe el nombre del archivo
    POST: Le permite al usuario modificar el archivo
    """
    
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
    """
    PRE: Recibe la ruta actual
    POST: Muestra el menu para que el usuario decida lo que quiera crear
    """
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

def crear_carpeta_sobrantes(directorio_evaluacion: str)->None:
    '''
    PRE: Recibo el directorio donde estan las evaluaciones
    POST: Para los alumnos no matcheados se les crea una carpeta aparte donde seran guardados sus examenes
    '''
    os.mkdir(directorio_evaluacion + SEP + "sobrantes")
    alumnos_sobrantes = directorio_evaluacion + SEP + "sobrantes" + SEP
    ruta_alumnos_sobrantes = os.getcwd() + SEP + "evaluacion" + SEP
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
        ruta_alumno = directorio_evaluacion + SEP + profesor + SEP
        ruta_evaluaciones = os.getcwd() + SEP + "evaluacion" + SEP + alumno + SEP
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
        os.mkdir(directorio_evaluacion + SEP + profesor)

        crear_carpeta_alumnos(dict_docentes,directorio_evaluacion, profesor)

    crear_carpeta_sobrantes(directorio_evaluacion)
    shutil.rmtree(os.getcwd() + SEP + "evaluacion")

def crear_carpeta_evaluacion(ruta: str)->None: 
    '''
    PRE: Recibe la ruta de la ubicacion donde se encuentra el usuario
    POST: usando las distintas funciones para anidar crea la carpeta de la evaluacion
    '''
    nombre_ev = input("Nombre de la evalucaion: ")
    archivo_alumnos = input("\nIngrese el nombre del archivo de los alumnos con su extension: ")
    archivo_docentes = input("\nIngrese el nombre del archivo de los docentes con su extension: ")
    print("\nIngrese el nombre del nuevo archivo que se creara con la relacion docentes/alumnos")
    archivo_docente_alumno = input(" -> ")

    nombre_csv_DA = archivo_docente_alumno + ".csv"
    crear_archivo_alumnos_docentes(archivo_alumnos, archivo_docentes,nombre_csv_DA)

    ruta_ev = ruta + SEP + nombre_ev
    os.mkdir(ruta_ev)

    os.getcwd()
    
    crear_carpeta_profesores(nombre_csv_DA, ruta_ev)

# --------------------- RECEPCION DE EVALUACIONES ---------- 
def obtener_email( id_mensaje:str ):
    '''
    PRE: recibe id de un correo en especifico 
    POST: obtiene desde gmail un correo en especifico 
    '''
    servicio = service_gmail.obtener_servicio()
    mensaje = servicio.users().messages().get(userId='me',id=id_mensaje).execute()
    return mensaje

def obtener_lista_email():
    '''
    PRE: obtiene los filtros para la busqueda de los correos 
    POST: obtiene desde gmail todos los correos segun los filtros aplicados 
    '''
    fecha = obtener_fecha() 
    servicio = service_gmail.obtener_servicio()
    resultados = servicio.users().messages().list(userId='me', q='in:inbox is:unread ' + fecha).execute()
    return resultados.get('messages',[])

def enviar_email( email:str, msj:str):
    '''
    PRE: recibe un email y un mensaje string
    POST: envia un correo a email ingresado con el mensaje que pasa por parametro 
    '''
    try:
        servicio = service_gmail.obtener_servicio()
        mime_mensaje = MIMEMultipart()
        mime_mensaje['subject'] = 'EVALUACION'
        mime_mensaje['to'] = email
        mime_mensaje.attach(MIMEText(msj, 'plain'))
        raw_string = base64.urlsafe_b64encode(mime_mensaje.as_bytes()).decode()
        mensaje = servicio.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    except:
        print("OCURRIO UN PROBLEMA AL ENVIAR EL SIGUIENTE MENSAJE: ")
        print(msj)

def enviar_email_adjunto( email:str, msj:str, adjunto:str):
    '''
    PRE: recibe un email y un mensaje string y un archivo pdf 
    POST: envia un correo a email ingresado con el mensaje que pasa por parametro y el archivo 
    '''
    try:
        servicio = service_gmail.obtener_servicio()
        mime_mensaje = MIMEMultipart()
        mime_mensaje['subject'] = 'EVALUACION'
        mime_mensaje['to'] = email
        mime_mensaje.attach(MIMEText(msj, 'plain'))
        
        temp = open(adjunto, 'rb')
        attachement = MIMEApplication(temp.read(), _subtype="pdf")
        temp.close()
        
        # se codifica el archivo para su envio 
        encoders.encode_base64(attachement)
        filename = os.path.basename(adjunto)
        attachement.add_header('Content-Disposition', 'attachment', filename=filename)
        mime_mensaje.attach(attachement) 

        mensaje_bytes = mime_mensaje.as_bytes() 
        mensaje_base64 = base64.urlsafe_b64encode(mensaje_bytes)
        raw = mensaje_base64.decode() 
        mensaje = servicio.users().messages().send(userId='me', body={'raw': raw}).execute()
    except:
        print("OCURRIO UN PROBLEMA AL ENVIAR EL SIGUIENTE MENSAJE: ")
        print(msj)

def descomprimir_archivo(name:str,email:str):
    '''
    PRE: recibe un el nombre de un archivo y el email de el usuario
    POST: descomprime un archivo zip para luego ponerle el nombre en los parametros 
    '''
    validar = True
    archivo = "./evaluacion/"+name+".zip"
    try:
        with ZipFile(archivo, 'r') as evaluacion:
            nombres_archivo = evaluacion.namelist()
            for nombre_archivo in nombres_archivo: 
                if nombre_archivo.endswith('.py'):
                    evaluacion.extract(nombre_archivo, 'evaluacion/'+name)
                    print("ARCHIVO DESCOMPRIMIDO")
                else:
                    validar = False
                    enviar_email(email,'FORMATO DE ARCHIVOS INCORRECTO - '+nombre_archivo)
                    print("FORMATO DE ARCHIVOS INCORRECTO: " + email)
    except:
        validar = False
        enviar_email(email,'OCURRIO UN PROBLEMA AL DESCOMPRIMIR EL ZIP')
        print("OCURRIO UN PROBLEMA AL DESCOMPRIMIR EL ZIP: " + email)
    return validar        

def obtener_adjunto(email,msj_id,titulo,email_alumno):
    '''
    PRE: recibe un email y la informacion del usuario 
    POST: obtiene un archivo de un correo en especifico
    '''
    validar = True
    msj_email = ""
    msj_error = ""
    servicio = service_gmail.obtener_servicio()
    if 'parts' in email['payload' ]:        
        for adjunto in email['payload']['parts']:
            mime_type = adjunto['mimeType']
            nombre_archivo = adjunto['filename']
            body = adjunto['body']
            # si viene un archivo adjunto lo obtenemos 
            if 'attachmentId' in body:
                try:
                    attachment_id = adjunto['body']['attachmentId']
                    resultado = servicio.users().messages().attachments().get(userId='me', messageId=msj_id,id=attachment_id).execute()
                    adjunto_data = resultado['data']
                    archivo = base64.urlsafe_b64decode(adjunto_data.encode('UTF-8'))

                    #creamos el archivo en local 
                    with open("./evaluacion/"+nombre_archivo, 'wb') as f:
                        f.write(archivo)
                    validar = descomprimir_archivo(titulo,email_alumno)
                except:
                    validar = False
                    msj_email = "OCURRIO UN PROBLEMA AL DESCARGAR EL ZIP"
                    msj_error = "OCURRIO UN PROBLEMA AL DESCARGAR EL ZIP: " + email_alumno    
            else:
                validar = False
                msj_email = 'FALTA ADJUNTO'
                msj_error = "FALTA ADJUNTO: " + email_alumno
    else:
        validar = False
        msj_email = 'OCURRIO UN PROBLEMA CON EL CORREO'
        msj_error = "OCURRIO UN PROBLEMA CON EL CORREO : " + email_alumno   
    enviar_email(email_alumno,msj_email)    
    return validar        

def validate_opcion(limite:int,text:str) -> int :
    '''
    PRE: recibe un limite para un numero y una opcion que deberia ser un numero  
    POST: valida que la opcion sea numerica y entre en el limite definido  
    '''
    opcion = input(text)
    
    while not opcion.isnumeric() or not (0 < int(opcion) <= limite) :      
        print("La opción ingresada, no es valida")
        opcion = input(text)

    return int(opcion)   

def obtener_fecha():
    '''
    PRE: se ingresa la fecha con sus respectivas validaciones 
    POST: se obtiene una fecha con el formato para filtrar en gmail 
    '''
    print("A continuacion ingresaras la fecha de las evaluacionesa a obtener")
    mes = validate_opcion(12,"Ingrese mes ( 1 al 12 ) :")
    dia = validate_opcion(31,"Ingrese dia ( 1 al 31 ) :")
    fecha = str(dia) + "-" + str(mes) + "-" + "2021"
    formato_fecha = "%d-%m-%Y"
    fecha_inicial = datetime.strptime(fecha, formato_fecha)
    fecha_antes = fecha_inicial + timedelta(days=1)
    fecha_despues = fecha_inicial - timedelta(days=1)
    return "after:2021/"+str(fecha_despues.month)+SEP+str(fecha_despues.day)+" before:2021/"+str(fecha_antes.month)+SEP+str(fecha_antes.day)

def obtener_evaluaciones():
    '''
    PRE: recibe los emails de una fecha en especifico  
    POST: se operan por separado cada correo y se validad los formatos necesarios para obtener archivos y crear las
    carpetas de evaluaciones 
    '''
    mensajes = obtener_lista_email()
    email = ''
    titulo = ''
    fecha = ''  
    validar = True
    for msj in mensajes:
        msj_id = msj['id']
        msj_detalles = obtener_email(msj_id)
        if 'payload' in msj_detalles:
            for msj_detalle in msj_detalles["payload"]["headers"]: 
                if msj_detalle["name"].lower() == 'to':
                    email = msj_detalle["value"]
                if msj_detalle["name"].lower() == 'subject':   
                    titulo = msj_detalle["value"]
            #validamos formato [nombre] [apellido]
            if validar_nombre(titulo):    
                validar = obtener_adjunto(msj_detalles,msj_id,titulo,email)
                if validar:
                    enviar_email(email,'ENTREGA OK')  
            else:
                print("FORMATO DE NOMBRE INVALIDO: " + email)        
                enviar_email(email,'FORMATO DE NOMBRE INVALIDO')
        else:
            print("OCURRIO UN PROBLEMA CON EL CORREO: " + email)        

def validar_nombre(text:str) -> str :
    '''
    PRE: se obtiene nombre del titulo del gmail  
    POST: se valida el formato de el titulo que sean solo letras 
    '''
    validar = True
    alumno = text.split()
    for nombre in alumno: 
        if not nombre.isalpha():     
            validar = False
    return validar

def main()-> None:
    ruta_actual = RUTA
    mostrar_menu(ruta_actual)
    opcion = input("opcion : ")


    while (opcion[0] != "8"):
        opcion = opcion.split(" ")
        # --------  Navegacion :
        if opcion[0] == "cd" or opcion[0] == ".." :
            comando = opcion
            ruta_actual = recorrer_directorio(ruta_actual, comando)
        elif opcion[0] == "mv.remoto":
            drive.mover_archivos()
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
                
            elif eleccion != "5":
                ## subo el archivo a drive
                print("\n --- Suba el archivo recien creado a su drive ---  ")
                print("Ingrese el nombre del archivo recien creado con la extension -> ej: texto.txt")
                nombre_archivo = input("Archivo: ")
                ruta_archivo = RUTA + SEP + nombre_archivo
                carpeta_contenedora = ruta_actual.split(SEP)[-1]
                drive.opciones_subir_archivos(nombre_archivo, ruta_archivo, carpeta_contenedora)

        elif opcion[0] == "3":

            elegir = input("\n1 - Subir archivo\n2 - Subir carpeta\n -> ")
            carpeta = RUTA.split(SEP)[-1]
            if elegir == "1":
                print(" ------ Navega por tu drive y subi el archivo a donde quieras !  ------ ")
                nombre_archivo = input("Ingrese el nombre del archivo que quiera subir : ")
                ruta_actual = RUTA + SEP + nombre_archivo
                try: 
                    
                    drive.menu_subir_archivos(ruta_actual, nombre_archivo, carpeta, 'archivo')
                    print(f" ### El archivo {nombre_archivo} subio exitosamente ### ")
                except :
                    print("\n ### No se puede subir un archivo inexistene ### ")
            elif elegir == "2":
                try: 
                    carpeta_a_subir = input("Ingrese el nombre de la carpeta que desea subir\n -> ")
                    ruta = os.getcwd() + SEP + carpeta_a_subir
                    drive.menu_subir_archivos(ruta, carpeta_a_subir, carpeta, 'carpeta')
                    print(f" ### La carpeta {carpeta_a_subir} se subio exitosamente ### ")
                except :
                    print("\n ### No se puede subir una carpeta inexistene ### ")

        elif opcion[0] == "4":
            drive.menu_descargar_elementos(ruta_actual)

        elif opcion[0] == "5":
            nombre_carpeta = RUTA.split(SEP)[-1]
            print(f"\n Sincroniza {nombre_carpeta}")
            sincronizacion = input(f"Desea sincronizar la carpeta {nombre_carpeta} (s/n): ")
            if sincronizacion == "s":
                    c_id = drive.encontrar_carpeta_upstream(nombre_carpeta)[0]
                    archivos_remoto = drive.fecha_modificacion_remoto(c_id)
                    archivos_local = drive.fecha_modificacion_local(ruta_actual)[0]
                    carpeta_local = drive.fecha_modificacion_local(ruta_actual)[1]
                    drive.sincronizar(archivos_remoto,archivos_local, carpeta_local, ruta_actual)

        elif opcion[0] == "6":
            email_usuario = input("Introduzca su email para enviarle las instrucciones: ")
            enviar_email_adjunto(email_usuario,"INSTRUCCIONES",ruta_actual + SEP + "instrucciones.pdf")
            obtener_evaluaciones()

        elif opcion[0] == "7":
            crear_carpeta_evaluacion(ruta_actual)

        mostrar_menu(ruta_actual)
        opcion = input("opcion : ")

main()
