import os
import sys
import shutil
from io import StringIO

HOME = os.getcwd() + "/Index"

def CrearArchivo(nombre, ruta):
    print("Crear archivo")
    try:
        with open(ruta + nombre + ".txt", "x") as archivo:
            print("\t" + "El archivo " + nombre + " se ha creado")
    except:
        print("\t" + "El archivo " + nombre + " ya existe.")

def RenombrarArchivo(ruta):
    nombreArchivo = SeleccionarArchivo(os.listdir(ruta), "renombrar", False)

    if(nombreArchivo == ""):
        input("\t No hay archivos en este directorio. Pulsa enter para continuar ... ")
        return

    nuevoNombre = input( "\t Ingresa el nuevo nombre para '" + nombreArchivo + "': ")
    
    CopiarArchivo(ruta + "/" + nombreArchivo, ruta + "/" + nuevoNombre + ".txt")

def ModificarArchivo(ruta):
    nombreArchivo = SeleccionarArchivo(os.listdir(ruta), "modificar", False)
    if(nombreArchivo == ""):
        input("\t No hay archivos en este directorio. Pulsa enter para continuar ... ")
        return
    
    nuevoContenido = input("\t Ingresa el nuevo contenido para el archivo " + nombreArchivo + ": ")    
    with open(ruta + nombreArchivo, "w") as archivo:
        archivo.write(nuevoContenido)

def BorrarArchivo(ruta):
    nombreArchivo = SeleccionarArchivo(os.listdir(ruta), "eliminar", False)

    if(nombreArchivo == ""):
        input("\t No hay archivos en este directorio. Pulsa enter para continuar ... ")
        return
    
    opcion = input("\t Eliminar archivo? Y/n: ")
    if( opcion.lower() == "y"):
        os.remove(ruta + nombreArchivo)

def CrearDirectorio(ruta, nombre):    
    if( not os.path.exists(ruta + nombre + "/") ):
        os.mkdir(ruta + nombre + "/")
        print( "\t" + "El directorio " + nombre + " se ha creado")
    else:
        print( "\t" + "El directorio " + nombre + " ya existe")

def BorrarDirectorio(ruta):
    contenidos = os.listdir(ruta)
    
    for contenido in contenidos:
        if("." in contenido):
            os.remove(ruta + "/" + contenido)
        else:
            BorrarDirectorio(ruta + "/" + contenido)
    os.rmdir(ruta)

def RenombrarDirectorio(nuevoDirectorio, ruta):
    contenidos = os.listdir(ruta)
    for contenido in contenidos:
        if("." in contenido):                        
            CopiarArchivo(ruta + "/" + contenido, nuevoDirectorio + "/" + contenido)            
        else:
            CrearDirectorio(nuevoDirectorio + "/",contenido)
            RenombrarDirectorio(nuevoDirectorio + "/" + contenido, ruta + "/" + contenido)
    os.rmdir(ruta)

def CopiarArchivo(original, copia):
    contenido = ""
    with open(original, "r") as archivo1:
        contenido = archivo1.read()

    with open(copia, "w") as archivo2:
        archivo2.write(contenido)

    os.remove(original)

def ListarDirectorio(ruta):
    print( "Archivos en el directorio " + ( ruta.replace(HOME, "") ) )
    print( "\t" + str(os.listdir(ruta)) )

def AbrirArchivo(ruta):
    nombreArchivo = SeleccionarArchivo(os.listdir(ruta), "abrir", False)
    with open(ruta + nombreArchivo, "r") as archivo:
        print("\tContenido: ")
        contenido = archivo.read()        
        print( "\t'" + contenido.replace("\n","\n\t")+ "'")
    input("\tPulsa enter para continuar ... ")

def AbrirDirectorio(ruta):
    directorio = SeleccionarArchivo(os.listdir(ruta), "abrir", True)
    
    if( directorio == ""):
        input("\t No hay directorios. Pulsa enter para continuar ... ")
        return ""
    return directorio

def RegresarDirectorio(ruta):
    print("Regresar")
    if( ruta.replace(HOME,"") != "/"):
        arrayRuta = ruta.replace(HOME,"").split("/")
        rActual = ""
        for i in range(0, len(arrayRuta) - 2):
            rActual = rActual + arrayRuta[i] + "/"
        return rActual
    return "/"

def SeleccionarArchivo(archivos, accion, esDirectorio = False):
    while(True):
        i = 0
        files = []
        directorios = []
        
        for archivo in archivos:            
            if( "." in archivo ):
                files.append(archivo)
            else:
                directorios.append(archivo)

            if(not esDirectorio and "." in archivo):
                print( "\t" + str( len(files) ) + ". " + archivo)
            elif(esDirectorio and "." not in archivo):
                print( "\t" + str( len(directorios) ) + ". " + archivo)

        if( (len(files) == 0 and not esDirectorio) or (len(directorios) == 0 and esDirectorio) ):
            return ""

        if(esDirectorio):
            aux = directorios
        else:
            aux = files

        opcion = input( "\t Ingresa el numero del archivo que deseas " + accion + ": ")
        if( opcion.isdigit() ):
            numArchivo = int(opcion)
            if(numArchivo > 0 and numArchivo <= len(aux)):
                if(esDirectorio):
                    return directorios[numArchivo - 1]
                return files[numArchivo - 1]
        print("\t Selecciona una opción valida")

ruta = "/"
while(True):    
    os.system("clear")
    ListarDirectorio(HOME + ruta)

    print("1. Crear archivo")
    print("2. Ver archivo")
    print("3. Modificar contenido del archivo")
    print("4. Renombrar archivo")
    print("5. Borrar archivo")
    print("6. Crear directorio")
    print("7. Abrir directorio")
    print("8. Borrar directorio")
    print("9. Renombrar directorio")
    print("10. Directorio anterior")
    print("11. Salir")
    
    opcion = input(" Ingresa una opción: ")

    if( opcion == "1"):
        nombre = input( "Ingresa el nombre del archivo de texto: ")
        CrearArchivo(nombre.replace(" ", ""), HOME  + ruta)
    elif( opcion == "2"):
        AbrirArchivo(HOME + ruta)
    elif( opcion == "3"):
        ModificarArchivo(HOME + ruta)
    elif( opcion == "4"):
        RenombrarArchivo(HOME + ruta)
    elif( opcion == "5"):
        BorrarArchivo(HOME + ruta)
    elif( opcion == "6"):
        nombre = input( "\tIngresa el nombre del directorio: ")
        CrearDirectorio(HOME + ruta, nombre)
    elif( opcion == "7"):
        directorio = AbrirDirectorio(HOME + ruta)
        if(directorio != ""):
            ruta = ruta + directorio + "/"
    elif( opcion == "8"):
        directorio = SeleccionarArchivo(os.listdir(HOME + ruta), "eliminar", True)
        if(directorio == ""):
            input("\t No hay directorios. Pulsa enter para continuar ... ")
        else:
            opcion = input("\t Eliminar directorio? Y/n: ")
            if( opcion.lower() == "y"):
                BorrarDirectorio(HOME+ruta+directorio)
    elif( opcion == "9"):
        directorio = SeleccionarArchivo(os.listdir(HOME + ruta), "renombrar", True)
        nuevoDiretorio = input( "\tIngresa el nuevo nombre para " + directorio + " : ")
        CrearDirectorio(HOME + ruta, nuevoDiretorio)        
        RenombrarDirectorio(HOME + ruta + nuevoDiretorio, HOME + ruta + directorio)
    elif( opcion == "10"):
        ruta = RegresarDirectorio(HOME + ruta)
    elif( opcion == "11"):
        break
    else:
        print("Ingresa una opción valida")
        input("Pulsa enter para continuar")
print("Saliendo ... ")