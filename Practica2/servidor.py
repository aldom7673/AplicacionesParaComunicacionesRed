#!/usr/bin/env python3

import socket
import time
import pickle
import random
import os
import datetime

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65433  # Port to listen on (non-privileged ports are > 1023)
buffer_size = 1024

#Inicializar tablero de acuerdo a la dificultad ingresada
def InicializarTablero( nivel ):
    for i in range ( 0, nivel):
        aux = []
        for j in range ( 0, nivel):
            aux.append( '' )
        tablero.append(aux)

def ImprimirTablero():
    linea = ""
    for i in range(0, 4*l - 3):
        linea += "_"

    for i in range(0, l):
        for j in range(0, l):
            dato = " " if (tablero[i][j] == "") else tablero[i][j]
            barra = " | " if (j < l - 1) else "  " 
            print(dato + barra,end='')
        if i < l - 1:
            print("\n" + linea)
    print("\n")

def VerificarTiro( tiroCliente, l):
    coordenadas = tiroCliente.split(',')
    if( len(coordenadas) == 2 ):
        if( set(coordenadas[0]).issubset(set(X_Validas)) and coordenadas[0] != '' and 
            set(coordenadas[1]).issubset(set(Y_Validas)) and coordenadas[1] != ''):
                return AsignarCoordenadas( int( coordenadas[1] ) - 1, ord( coordenadas[0] ) - 65 , l)

    #MostrarMensaje( "Datos no validos, verifice el formato de ingreso. Presiona enter para continuar...")
    return False

def AsignarCoordenadas(x, y, l):    
    if( tablero[x][y] == ''):
        tablero[x][y] = "X" if (turnoServidor) else "O"
        posicion = y + 1 + l * x
        if( posicion in listaPosicionesLibres ):
            listaPosicionesLibres.remove(posicion)
        return VerificarTablero(x, y, l)
    #MostrarMensaje( "La casilla ya esta ocupada, por favor, seleccione otra. Presiona enter para continuar...")    
    return False

def MostrarMensaje( mensaje ):
    input( mensaje )

def VerificarTablero(x, y, l):    
    simbolo = "X" if (turnoServidor) else "O"
    lineaCompletada = True

    #Compara horizontalmente
    for j in range (0, l):
        if( tablero[x][j] != simbolo ):
            lineaCompletada = False
            break

    #Compara verticalmente
    if(not lineaCompletada):
        lineaCompletada = True
        for i in range (0, l):
            if( tablero[i][y] != simbolo ):
                lineaCompletada = False
                break

    #Diagonalmente 0,0 a l,l
    if(not lineaCompletada and x == y):
        lineaCompletada = True
        for i in range (0, l):
            if( tablero[i][i] != simbolo ):
                lineaCompletada = False
                break

    #Diagonalmente 0, l-1 a l-1, 0
    if(not lineaCompletada and (x + y) == (l - 1)):
        lineaCompletada = True
        for i in range (0, l):
            if( tablero[i][l - 1 - i] != simbolo ):
                lineaCompletada = False
                break

    if(not lineaCompletada and len(listaPosicionesLibres) >  0):
        return True
    
    os.system("clear")
    if(turnoServidor and lineaCompletada):
        resultado = "El servidor ha ganado"
        print( "El servidor ha ganado" )
    if (not turnoServidor and lineaCompletada):
        resultado = "Usted ha ganado"
        print( "El cliente ha ganado" )
    if( not lineaCompletada ):
        print( "El juego ha terminado en empate" )
        resultado = "El juego ha terminado en empate"

    fin = datetime.datetime.now()
    tiempo = fin - inicio

    datoEnviar = []
    datoEnviar = tablero.copy()
    datoEnviar.append("FIN")
    datoEnviar.append(resultado)
    datoEnviar.append(str(tiempo))
    Client_conn.sendall(pickle.dumps(datoEnviar))

    global JUEGO_TERMINADO
    JUEGO_TERMINADO = True    
    return JUEGO_TERMINADO

def TirarServidor( l ):
    tiroServidor = random.choice(listaPosicionesLibres)
    x = ( l if (tiroServidor % l == 0) else tiroServidor % l ) - 1
    y =  int( (tiroServidor - 1) / l) 
    if( not AsignarCoordenadas(y, x, l) ):
        TirarServidor( l )

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("El servidor TCP está disponible y en espera de solicitudes")
    
    while True:
        print("Esperando al cliente")
        Client_conn, Client_addr = TCPServerSocket.accept()
        with Client_conn:
            print("Conectado a", Client_addr)        
            
            print("Esperando el nivel de juego ... ")
            nivel = Client_conn.recv(buffer_size)            
            print ("Recibido, nivel escogido : ", nivel,"   de : ", Client_addr)
            
            inicio = datetime.datetime.now()
            
            if not nivel:
                break

            listaPosicionesLibres =  []
            X_Validas = ['A','B','C']
            Y_Validas = ['1','2','3']

            if( int( nivel ) == 1 ):
                l = 3
            else:
                l = 5
                X_Validas.append('D','E')
                Y_Validas.append('4','5')

            for i in range (1, l * l + 1):
                listaPosicionesLibres.append(i)

            tablero = []
            InicializarTablero( l )
            JUEGO_TERMINADO = False
            turnoServidor = False

            #Enviando tablero y turno            
            while( not JUEGO_TERMINADO):
                os.system("clear")
                ImprimirTablero()
                if(turnoServidor):
                    TirarServidor( l )             
                    turnoServidor =  not turnoServidor
                else:
                    datoEnviar = []
                    datoEnviar = tablero.copy()
                    datoEnviar.append(turnoServidor)

                    Client_conn.sendall(pickle.dumps(datoEnviar))
                    print("Esperando tiro del cliente ", Client_addr)
                    tiroCliente = Client_conn.recv(buffer_size)                     
                    if ( VerificarTiro( pickle.loads(tiroCliente), l)):
                        ImprimirTablero()
                        turnoServidor = not turnoServidor