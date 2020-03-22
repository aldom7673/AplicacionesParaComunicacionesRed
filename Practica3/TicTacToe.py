import random

#Inicializar tablero de acuerdo a la dificultad ingresada
def InicializarTablero( nivel ):
    for i in range ( 0, nivel):
        aux = []
        for j in range ( 0, nivel):
            aux.append( '' )
        tablero.append(aux)

def TirarServidor( l ):
    tiroServidor = random.choice(listaPosicionesLibres)
    x = ( l if (tiroServidor % l == 0) else tiroServidor % l ) - 1
    y =  int( (tiroServidor - 1) / l) 
    if( not AsignarCoordenadas(y, x, l) ):
        TirarServidor( l )

def MostrarMensaje( mensaje ):
    input( mensaje )

def VerificarTiro( tiroCliente, l):
    coordenadas = tiroCliente.split(',')
    if( len(coordenadas) == 2 ):
        if( set(coordenadas[0]).issubset(set(X_Validas)) and coordenadas[0] != '' and 
            set(coordenadas[1]).issubset(set(Y_Validas)) and coordenadas[1] != ''):
                return AsignarCoordenadas( int( coordenadas[1] ) - 1, ord( coordenadas[0] ) - 65 , l)

    MostrarMensaje( "Datos no validos, verifice el formato de ingreso. Presiona enter para continuar...")
    return False

def AsignarCoordenadas(x, y, l):    
    if( tablero[x][y] == ''):
        tablero[x][y] = "X" if (turnoServidor) else "O"
        posicion = y + 1 + l * x
        if( posicion in listaPosicionesLibres ):
            listaPosicionesLibres.remove(posicion)
        return VerificarTablero(x, y, l)
    MostrarMensaje( "La casilla ya esta ocupada, por favor, seleccione otra. Presiona enter para continuar...")    
    return False

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

    if(not lineaCompletada):
        return True

    if(turnoServidor):
        print("El servidor ha ganado")
    else:
        print("El cliente ha ganado")
    ImprimirTablero()
    exit(0)

def ImprimirTablero():    
    for i in range(0, l):
        for j in range(0, l):
            dato = " " if (tablero[i][j] == "") else tablero[i][j]
            barra = " | " if (j < l - 1) else "  " 
            print(dato + barra,end='')
        if i < l - 1:
            print("\n__________")
    print("\n")

#Establecer dificultad de juego
nivel = input( "Ingresa el nivel de juego \n 1 - Principiante \n 2 - Avanzado\n Nivel : " )
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

tablero = []
InicializarTablero( l )
contadorDeCeldas = 0
turnoServidor = False

while( contadorDeCeldas < l*l ):
    ImprimirTablero()
    if(turnoServidor):
        TirarServidor( l )
        turnoServidor =  not turnoServidor
        contadorDeCeldas += 1
    else:
        tiroCliente = input( "Ingresa la coordenada de tu casilla con el formato letra,numero : ")
        if ( VerificarTiro( tiroCliente, l)):
            turnoServidor = not turnoServidor
            contadorDeCeldas += 1