# !/usr/bin/env python3

import socket
import sys
import threading
import datetime
import pickle
import os
import random

BUFFER_SIZE = 1024

#Inicializar tablero de acuerdo a la dificultad ingresada
def InicializarTablero( nivel ):
    tablero = []
    for i in range ( 0, nivel):
        aux = []
        for j in range ( 0, nivel):
            aux.append( '' )
        tablero.append(aux)
    return tablero

#Imprime el tablero de juego
def ImprimirTablero(tablero, l ):
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

#Tiro del servidor
def TirarServidor(tablero, l, listaPosicionesLibres, ES_TURNO_SERVIDOR, JUEGO_TERMINADO):
    tiroServidor = random.choice(listaPosicionesLibres)
    x = ( l if (tiroServidor % l == 0) else tiroServidor % l ) - 1
    y =  int( (tiroServidor - 1) / l)

    if( not AsignarCoordenadas(y, x, l, tablero, listaPosicionesLibres, ES_TURNO_SERVIDOR, JUEGO_TERMINADO) ):
        return TirarServidor(tablero, l, listaPosicionesLibres, ES_TURNO_SERVIDOR, JUEGO_TERMINADO)    
    return tiroServidor

#Verifica el tiro ingresado por el cliente
def VerificarTiro( tiroCliente, l, tablero, listaPosicionesLibres, ES_TURNO_SERVIDOR, X_Validas, Y_Validas, JUEGO_TERMINADO):
    coordenadas = tiroCliente.split(',')
    if( len(coordenadas) == 2 ):
        if( set(coordenadas[0]).issubset(set(X_Validas)) and coordenadas[0] != '' and 
            set(coordenadas[1]).issubset(set(Y_Validas)) and coordenadas[1] != ''):
                return AsignarCoordenadas( int( coordenadas[1] ) - 1, ord( coordenadas[0] ) - 65 , l, tablero, listaPosicionesLibres, ES_TURNO_SERVIDOR, JUEGO_TERMINADO)

    #MostrarMensaje( "Datos no validos, verifice el formato de ingreso. Presiona enter para continuar...")
    return False

#Asigna a la casilla (x,y) el tiro del jugador
def AsignarCoordenadas(x, y, l, tablero, listaPosicionesLibres, ES_TURNO_SERVIDOR, JUEGO_TERMINADO):
    if( tablero[x][y] == ''):
        tablero[x][y] = "X" if (ES_TURNO_SERVIDOR) else "O"
        posicion = y + 1 + l * x
        if( posicion in listaPosicionesLibres ):
            listaPosicionesLibres.remove(posicion)
        return True#VerificarTablero(x, y, l, tablero, listaPosicionesLibres, ES_TURNO_SERVIDOR, JUEGO_TERMINADO)
    #MostrarMensaje( "La casilla ya esta ocupada, por favor, seleccione otra. Presiona enter para continuar...")    
    return False

def VerificarTablero(x, y, l, tablero, listaPosicionesLibres, ES_TURNO_SERVIDOR, JUEGO_TERMINADO):
    simbolo = "X" if (ES_TURNO_SERVIDOR) else "O"
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
        return JUEGO_TERMINADO

    if(ES_TURNO_SERVIDOR and lineaCompletada):
        resultado = "El servidor ha ganado"
        print( "El servidor ha ganado" )
    if (not ES_TURNO_SERVIDOR and lineaCompletada):
        resultado = "Usted ha ganado"
        print( "El cliente ha ganado" )
    if( not lineaCompletada ):
        print( "El juego ha terminado en empate" )
        resultado = "El juego ha terminado en empate"

    tablero.append("FIN")
    tablero.append(resultado)    

    JUEGO_TERMINADO = True
    return JUEGO_TERMINADO

def servirPorSiempre(socketTcp, listaconexiones):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a", client_addr)
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(target=Jugar_gato, args=[client_conn, client_addr])
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    print(listaconexiones)


def Jugar_gato(conn, addr):
    try:
        cur_thread = threading.current_thread()        

        print("Esperando el nivel de juego ... ")
        nivel = conn.recv(BUFFER_SIZE)

        if not nivel:
            print("Error al recibir el nivel")
            exit(0)

        print ("Recibido, nivel escogido : ", nivel,"   de : ", addr)

        inicio = datetime.datetime.now()
        listaPosicionesLibres =  []
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

        for i in range (1, l * l + 1):
            listaPosicionesLibres.append(i)

        tablero = InicializarTablero( l )
        JUEGO_TERMINADO = False
        ES_TURNO_SERVIDOR = False

        while( not JUEGO_TERMINADO):            
            ImprimirTablero(tablero, l)

            if(ES_TURNO_SERVIDOR):
                tiroServidor = TirarServidor(tablero, l, listaPosicionesLibres, ES_TURNO_SERVIDOR, JUEGO_TERMINADO)
                x = ( l if (tiroServidor % l == 0) else tiroServidor % l ) - 1
                y =  int( (tiroServidor - 1) / l)
                JUEGO_TERMINADO = VerificarTablero(y, x, l, tablero, listaPosicionesLibres, ES_TURNO_SERVIDOR, JUEGO_TERMINADO)                
                ES_TURNO_SERVIDOR =  not ES_TURNO_SERVIDOR
            else:
                datoEnviar = []
                datoEnviar = tablero.copy()
                datoEnviar.append(ES_TURNO_SERVIDOR)
                conn.sendall(pickle.dumps(datoEnviar))
                print("Esperando tiro del cliente ", addr)
                tiroCliente = conn.recv(BUFFER_SIZE)                     
                if ( VerificarTiro( pickle.loads(tiroCliente), l, tablero, listaPosicionesLibres, ES_TURNO_SERVIDOR, X_Validas, Y_Validas, JUEGO_TERMINADO)):
                    coordenadas = pickle.loads(tiroCliente).split(',')                    
                    JUEGO_TERMINADO = VerificarTablero(int( coordenadas[1] ) - 1, ord( coordenadas[0] ) - 65, l, tablero, listaPosicionesLibres, ES_TURNO_SERVIDOR, JUEGO_TERMINADO)
                    ImprimirTablero(tablero, l)
                    ES_TURNO_SERVIDOR = not ES_TURNO_SERVIDOR

    
        fin = datetime.datetime.now()
        tiempo = fin - inicio
        tablero.append(str(tiempo))

        conn.sendall(pickle.dumps(tablero))
        print("Juego terminado con: ", addr)
        print("Resultado: ", tablero[l+1])
    except Exception as e:
        print(e)
    finally:
        conn.close()

listaConexiones = []
host, port, numConn = sys.argv[1:4]

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

serveraddr = (host, int(port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")
    print("HOST : " + host)
    print("PORT : " + port)
    servirPorSiempre(TCPServerSocket, listaConexiones)
