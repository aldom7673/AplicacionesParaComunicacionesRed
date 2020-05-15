import os
import xmlrpc.client
import datetime
s = xmlrpc.client.ServerProxy('http://localhost:8000')

def isFloat( n ):
    try:
        num = float( n )
        return True
    except:
        return False

while( True ):
    os.system("clear")
    operacion = ["Suma: a + b", "Resta: a - b", "Multiplicación: a * b", "División: a / b"]
    
    print( "Calculadora RPC" )
    print( "1. Suma" )
    print( "2. Resta" )
    print( "3. Multiplicación" )
    print( "4. División" )
    print( "5. Salir" )
    opcion = input( "Ingresa la operación que deseas realizar: ")

    if( opcion.isdigit() ):
        o = int( opcion )
        if( o > 0 and o <= 5):
            if( o == 5):
                break
            
            while(True):
                os.system("clear")
                print( operacion[o - 1])
                a = input( "Ingresa a ")
                b = input( "Ingresa b ")
                
                if( isFloat(a) and isFloat(b) ):
                    if( float(b) == 0 and o == 4):
                        input("b no puede ser cero. Pulsa enter para continuar ... ")
                    else:
                        break
                else:
                    input( "a y b deben ser números. Pulsa enter para continuar ... " )
            print("El resultado es :")
            if( o == 1):
                print( s.suma(float(a), float(b) ) )
            elif( o == 2 ):
                print( s.resta(float(a), float(b) ) )
            elif( o == 3 ):
                print( s.multiplicacion(float(a), float(b) ) )
            elif( o == 4 ):
                print( s.division(float(a), float(b) ) )                
            
            input( "Pulsa enter para continuar ... " )
        else:
            input( "Ingresa una opción valida. Pulsa enter para continuar ... " )