# !/usr/bin/env python3

import socket
import sys
import threading
import datetime
import pickle
import time

BUFFER_SIZE =  1024
l = 0
listaPosicionesLibres =  []
identificadores = []
X_Validas = ['A','B','C']
Y_Validas = ['1','2','3']
tablero = []    
JUEGO_TERMINADO = False
listaconexiones = []
id_Ganador = ""
inicio = datetime.datetime.now()
fin = ""

def ImprimirTablero():
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

#Inicializar tablero de acuerdo a la dificultad ingresada
def InicializarTablero( nivel ):
    tablero.clear()
    for i in range ( 0, nivel):
        aux = []
        for j in range ( 0, nivel):
            aux.append( '' )
        tablero.append(aux)

def ServirPorSiempre(socketTcp, numeroConexiones):
    global l
    try:
        condicionEsperarJugadores = threading.Condition()
        condicionTurnoActivo = threading.Condition()
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a", client_addr)

            client_conn.sendall(str(l).encode())
            if( l == 0):
                print("Esperando el nivel de juego ... ")
                nivel = client_conn.recv(BUFFER_SIZE)
                print ("Recibido, nivel escogido : ", nivel,"   de : ", client_addr)

            if( l == 0): # Se juega con el primer tablero que se haya creado
                inicio = datetime.datetime.now()
                if( int( nivel ) == 1 ):
                    l = 3
                else:
                    l = 5
                    X_Validas.append('D')
                    X_Validas.append('E')
                    Y_Validas.append('4')
                    Y_Validas.append('5')
                listaPosicionesLibres.clear()
                for i in range (1, l * l + 1):
                    listaPosicionesLibres.append(i)

                for i in range(1, int(numeroConexiones) + 1):
                    identificadores.append(str(i))

                InicializarTablero( l )
            listaconexiones.append(client_conn)
            identificador = identificadores[ len(listaconexiones) - 1 ]
            thread_read = threading.Thread(target=RecibirTiros, args=[client_conn, client_addr, identificador, condicionEsperarJugadores, condicionTurnoActivo, ])
            thread_read.start()
                
            with condicionEsperarJugadores:
                if(int(numeroConexiones) == len(listaconexiones)):
                    print("Se han conectado todos los jugadores")
                    thread_read_tiros = threading.Thread(target=GestionarTiros, args=[identificadores, condicionTurnoActivo, condicionEsperarJugadores, ])
                    thread_read_tiros.start()               
                else:
                    print("En espera de " + str(int(numeroConexiones) - len(listaconexiones)) + " conexiones")                    
                condicionEsperarJugadores.notifyAll()

            gestion_conexiones()
    except Exception as e:
        print(e)

def gestion_conexiones():
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    #print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    #print(listaconexiones)

def GestionarTiros(identificadores, condicionTurnoActivo, condicionEsperarJugadores):    
    global JUEGO_TERMINADO
    global TURNO_JUGADOR
    global l
    turnojugador = 0
    while(not JUEGO_TERMINADO):
        time.sleep(0.5)
        #Determina que jugador puede tirar
        with condicionTurnoActivo:
            TURNO_JUGADOR = identificadores[turnojugador % len(identificadores)]
            print("Turno del jugador " + TURNO_JUGADOR)            
            condicionTurnoActivo.notifyAll()
        #Espera a que el jugador notifique que termino su turno
        with condicionEsperarJugadores:
            condicionEsperarJugadores.wait()
        turnojugador += 1 
    
    with condicionTurnoActivo:
        condicionTurnoActivo.notifyAll()
    time.sleep(0.5)
    EnviarTableroAClientes(JUEGO_TERMINADO)
    tablero.clear()
    listaconexiones.clear()    
    l = 0
    print("hilos activos:", threading.active_count())
    JUEGO_TERMINADO = False

def VerificarTiro( tiroCliente, identificador):
    coordenadas = tiroCliente.split(',')
    if( len(coordenadas) == 2 ):
        if( set(coordenadas[0]).issubset(set(X_Validas)) and coordenadas[0] != '' and 
            set(coordenadas[1]).issubset(set(Y_Validas)) and coordenadas[1] != ''):
                return AsignarCoordenadas( int( coordenadas[1] ) - 1, ord( coordenadas[0] ) - 65 , l,  identificador)

    #MostrarMensaje( "Datos no validos, verifice el formato de ingreso. Presiona enter para continuar...")
    return False

def AsignarCoordenadas(x, y, l, identificador):
    if( tablero[x][y] == ''):
        tablero[x][y] = identificador
        posicion = y + 1 + l * x
        if( posicion in listaPosicionesLibres ):
            listaPosicionesLibres.remove(posicion)
        return True #VerificarTablero(x, y, l)
    #MostrarMensaje( "La casilla ya esta ocupada, por favor, seleccione otra. Presiona enter para continuar...")    
    return False

def VerificarTablero(x, y, identificador):
    simbolo = identificador
    lineaCompletada = True
    print( listaPosicionesLibres )
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
        return False

    global id_Ganador
    if( not lineaCompletada):
        id_Ganador = "-1"
        return True
    id_Ganador = identificador
    return True

def EnviarTableroAClientes(JUEGO_TERMINADO = False, identificador = ''):
    i = 0
    for conn in listaconexiones:
        datoEnviar = []
        datoEnviar = tablero.copy()
        if( JUEGO_TERMINADO ):
            datoEnviar.append('FIN')
            if( id_Ganador == "-1" ):
                datoEnviar.append( "El juego ha terminado en empate" )
            elif( id_Ganador == identificadores[i] ):
                datoEnviar.append( "Usted ha ganado" )
            else:
                datoEnviar.append( "Usted ha perdido" )
            fin = str( datetime.datetime.now() - inicio )
            datoEnviar.append("Tiempo de juego: " + fin)
            i += 1
        else:
            datoEnviar.append(JUEGO_TERMINADO)
            datoEnviar.append(identificadores[i] == identificador)
            datoEnviar.append(identificador)
            i += 1
        conn.sendall(pickle.dumps(datoEnviar))
        if(JUEGO_TERMINADO):
            print("Cerrando conexion " + str(i))
            conn.close()

def RecibirTiros(conn, addr, identificador, condicionEsperarJugadores, condicionTurnoActivo):
    global JUEGO_TERMINADO
    try:
        while True:
            with condicionEsperarJugadores:
                condicionEsperarJugadores.wait()
                if(conexiones == len(listaconexiones)):
                    print("Enviando inicio de juego")
                    conn.sendall( b'0' )
                    break
                else:
                    conn.sendall( str(conexiones - len(listaconexiones)).encode() )
        JUEGO_TERMINADO = False

        while not JUEGO_TERMINADO:
            with condicionTurnoActivo:
                condicionTurnoActivo.wait()
                if( TURNO_JUGADOR == identificador and not JUEGO_TERMINADO):
                    with condicionEsperarJugadores:
                        datoEnviar = []
                        datoEnviar = tablero.copy()
                        EnviarTableroAClientes(identificador=TURNO_JUGADOR)
                        print("Esperando tiro del cliente ", addr)
                        tiroCliente = conn.recv(BUFFER_SIZE)
                        if ( VerificarTiro( pickle.loads(tiroCliente), identificador)):
                            coordenadas = pickle.loads(tiroCliente).split(',')
                            JUEGO_TERMINADO = VerificarTablero(int( coordenadas[1] ) - 1, ord( coordenadas[0] ) - 65, identificador)
                        condicionEsperarJugadores.notify() #Notifica al gestor de tiros que el cliente ha tirado
                else:
                    print ("No es turno del jugador con identificador " + identificador)

    except Exception as e:
        print(e)
    finally:
        print("SALIENDO jugador " + identificador  +  " ... ")

host, port, numConn = sys.argv[1:4]

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

serveraddr = (host, int(port))
TURNO_JUGADOR = ''
conexiones = 0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    conexiones = int(numConn)
    print("El servidor TCP está disponible y en espera de solicitudes")
    ServirPorSiempre(TCPServerSocket, int(numConn))
