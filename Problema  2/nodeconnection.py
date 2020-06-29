import socket
import sys
import time
import threading
import random
import hashlib


class NodeConnection(threading.Thread):

    def __init__(self, main_node, sock, id, host, port):

        super(NodeConnection, self).__init__()

        self.host = host
        self.port = port
        self.main_node = main_node
        self.sock = sock
        self.terminate_flag = threading.Event()

        # Variable for parsing the incoming json messages
        self.buffer = ""

        # The id of the connected node
        self.id = id

        self.main_node.debug_print("Conexion de envio con cliente (" + self.id + ") '" + self.host + ":" + str(self.port) + "'")

    def send(self, data):
        
        try:
            data = data + "-TSN"
            self.sock.sendall(data.encode('utf-8'))

        except Exception as e:
            self.main_node.debug_print("Envio error:", sys.exc_info()[0])
            self.main_node.debug_print("Exception: " + str(e))
            self.terminate_flag.set()

    def stop(self):
        self.terminate_flag.set()


    def run(self):
        self.sock.settimeout(10.0)          
 
        while not self.terminate_flag.is_set():
            line = ""

            try:
                line = self.sock.recv(4096) 

            except socket.timeout:
                self.main_node.debug_print("timeout")

            except Exception as e:
                self.terminate_flag.set()
                self.main_node.debug_print("El socket se ha detenido (%s)" % line)
                self.main_node.debug_print(e)

            if line != "":
                try:
                    # BUG: possible buffer overflow when no -TSN is found!
                    self.buffer += str(line.decode('utf-8')) 

                except Exception as e:
                    print("Error en linea | " + str(e))

                index = self.buffer.find("-TSN")
                while index > 0:
                    message = self.buffer[0:index]
                    self.buffer = self.buffer[index + 4::]

                    self.main_node.message_count_recv += 1
                    self.main_node.node_message(self, message)

                    index = self.buffer.find("-TSN")

            time.sleep(0.01)

        self.sock.settimeout(None)
        self.sock.close()
        self.main_node.debug_print("Conexion detenida")

    def __str__(self):
        return 'NodeConnection: {}:{} <-> {}:{} ({})'.format(self.main_node.host, self.main_node.port, self.host, self.port, self.id)

    def __repr__(self):
        return '<NodeConnection: Node {}:{} <-> Connection {}:{}>'.format(self.main_node.host, self.main_node.port, self.host, self.port)
