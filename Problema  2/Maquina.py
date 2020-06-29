class Maquina():
    def __init__(self, nombre = "", ip = "", port = ""):
        self.IP = 0
        self.PORT = 1
        self.nombre = nombre
        self.caracteristicas = []
        self.caracteristicas.append(ip)
        self.caracteristicas.append(port)
        
    
    def DescripcionMaquina(self):
        print( "\t" + self.nombre + " [" + "Direccion: " + self.caracteristicas[self.IP] + ", Puerto: " + self.caracteristicas[self.PORT] + "]\n")
        return
