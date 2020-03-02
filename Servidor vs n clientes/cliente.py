#!/usr/bin/env python3

import socket
import pickle
import os
import datetime

HOST = ""  # The server's hostname or IP address
PORT = 0 # The port used by the server
buffer_size = 1024

HOST = input( "Ingresa la IP del servidor: ")

while(True):
    puerto = input( "Ingresa el puerto: " )
    if(puerto.isdigit()):
        if( int(puerto) > 1023 ):
            PORT = int(puerto)
            break
    input( "Verifica el puerto. Presiona enter para continuar ... ")

def ImprimirTablero(tablero):
    linea = "    "
    for i in range(0, 4*l - 3):
        linea += "_"

    letras ="    A   B   C"
    if(l == 5): 
        letras += "   D   E"
    print(letras)

    for i in range(0, l):
        print( i + 1, end='   ')
        for j in range(0, l):
            dato = " " if (tablero[i][j] == "") else tablero[i][j]
            barra = " | " if (j < l - 1) else "  " 
            print(dato + barra,end='')
        if i < l - 1:
            print("\n" + linea)
    print("\n")

def VerificarTiro( tiroCliente, l, tablero):
    coordenadas = tiroCliente.split(',')
    if( len(coordenadas) == 2 ):
        if( set(coordenadas[0]).issubset(set(X_Validas)) and coordenadas[0] != '' and  Y_Validas.count(coordenadas[1]) and coordenadas[1] != ''):
            if( tablero[int( coordenadas[1] ) - 1][ord( coordenadas[0] ) - 65] == ''):
                return True
            else:
                MostrarMensaje( "La casilla ya esta ocupada, por favor, seleccione otra. Presiona enter para continuar...")    
                return False

    MostrarMensaje( "Datos no validos, verifice el formato de ingreso. Presiona enter para continuar...")
    return False

def MostrarMensaje( mensaje ):
    input( mensaje )


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    print(HOST)
    print(PORT)
    TCPClientSocket.connect((HOST, PORT))
        
    while(True):
        nivel = input( "Ingresa el nivel de juego \n 1 - Principiante \n 2 - Avanzado\n Nivel : " )    
        if (nivel.isdigit()):
            if(0 < int(nivel) < 3):
                X_Validas = ['A','B','C']
                Y_Validas = ['1','2','3']

                if( int( nivel ) == 1 ):
                    l = 3
                else:
                    l = 5
                    X_Validas.append('D')
                    X_Validas.append('E')
                    Y_Validas.append('4')
                    Y_Validas.append('5')

                print("Enviando nivel de juego ...")
                TCPClientSocket.sendall(str.encode(nivel))
                break
        input( "Nivel no valido, por favor intenta de nuevo. Presiona enter para continuar..." )

    os.system("clear")
    print("Esperando tablero de juego ...")    
    while(True):
        datoRecibido = pickle.loads(TCPClientSocket.recv(buffer_size))
        if(datoRecibido[l] == 'FIN'):
            os.system("clear")
            print(datoRecibido[l+1])
            print("Tiempo de juego: " + datoRecibido[l+2])
            ImprimirTablero(datoRecibido)
            break

        if(not datoRecibido[l]): #Turno del cliente
            while(True):
                os.system("clear")
                ImprimirTablero(datoRecibido)
                tiroCliente = input( "Ingresa la coordenada de tu casilla con el formato letra,numero : ")                
                if( VerificarTiro(tiroCliente,l,datoRecibido) ):
                    TCPClientSocket.sendall(pickle.dumps(tiroCliente))
                    break
        else:
            print("Esperando tiro del servidor ...")
            