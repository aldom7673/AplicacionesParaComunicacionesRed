import logging
import threading
import time

def LeerBaseDatos(lock, numeroHilo):
    #print( "El hilo de lectura " + str(numeroHilo) + " intenta leer de la base de datos " )
    while True:
        have_it = lock.acquire(0)
        try:
            if have_it:
                print( "El hilo " + str(numeroHilo) + " de lectura ACCEDIO a al base de datos" )
                time.sleep(2)
            else:
                time.sleep(0.5)
                print( "El hilo " + str(numeroHilo) + " de lectura intento usar la base de datos" )
        finally:
            if have_it:
                lock.release()
                print( "El hilo " + str(numeroHilo) + " de lectura ha dejado de usar la base de datos" )
        time.sleep(1)

def EscribirBaseDatos(lock, numeroHilo):
    #print( "El hilo de escritura " + str(numeroHilo) + " intenta escirbir en base de datos " )
    while True:
        have_it = lock.acquire(0)
        try:
            if have_it:
                print( "El hilo " + str(numeroHilo) + " de escritura ACCEDIO a al base de datos" )
                time.sleep(3)
            else:
                print( "El hilo " + str(numeroHilo) + " de escritura intento acceder a la base de datos" )
                time.sleep(1)
        finally:
            if have_it:
                lock.release()
                print( "El hilo " + str(numeroHilo) + " de escritura ha dejado de usar la base de datos" )
        time.sleep(1)

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

lock = threading.Lock()

print("Creando hilos")

hiloLectura1 = threading.Thread(target=LeerBaseDatos, args=(lock, 1), name='LeerBaseDatos')
print("Iniciando hilo de lectura 1")
hiloLectura1.start()

hiloLectura2 = threading.Thread(target=LeerBaseDatos, args=(lock, 2), name='LeerBaseDatos')
print("Iniciando hilo de lectura 2")
hiloLectura2.start()

hiloEscritura1 = threading.Thread(target=EscribirBaseDatos, args=(lock, 1), name='EscribirBaseDatos')
print("Iniciando hilo de escritura 1")
hiloEscritura1.start()

hiloEscritura2 = threading.Thread(target=EscribirBaseDatos, args=(lock, 2), name='EscribirBaseDatos')
print("Iniciando hilo de escritura 2")
hiloEscritura2.start()

#holder = threading.Thread(target=lock_holder,args=(lock,), name='LockHolder', daemon=True,)
#holder.start()

#worker = threading.Thread(target=worker, args=(lock,), name='Worker',)
#worker.start()
