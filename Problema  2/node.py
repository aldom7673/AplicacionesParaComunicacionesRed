import socket
import sys
import time
import threading
import random
import hashlib

from nodeconnection import NodeConnection

class Node(threading.Thread):

    def __init__(self, host, port, callback=None):
        super(Node, self).__init__()

        # Al activarse la bandera el nodo se detendra
        self.terminate_flag = threading.Event()

        self.host = host
        self.port = port

        self.callback = callback

        # Nodes that have established a connection with this node
        self.nodes_inbound = []  # Nodes that are connect with us N->(US)->N

        # Nodes that this nodes is connected to
        self.nodes_outbound = []  # Nodes that we are connected to (US)->N

        # Crea un ID para cada nodo.
        id = hashlib.sha512()
        t = self.host + str(self.port) + str(random.randint(1, 99999999))
        id.update(t.encode('ascii'))
        self.id = id.hexdigest()

        # Iniciacion del servidor TCP/IP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.init_server()

        # Contadores de mensajes
        self.message_count_send = 0
        self.message_count_recv = 0
        self.messgaE_count_rerr = 0

        self.debug = False

    @property
    def all_nodes(self):
        return self.nodes_inbound + self.nodes_outbound

    def debug_print(self, message):
        if self.debug:
            print("DEBUG PRINT: " + message)

    def init_server(self):
        """Inicializacion del servidor TCP/IP para comenzar a recibir conexiones"""
        print("Inicializando nodo en puerto: " + str(self.port) + "\n")
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(10.0)
        self.sock.listen(1)

    def print_connections(self):
        print("Conexiones del nodo:")
        print("- Total nodes connected with us: %d" % len(self.nodes_inbound))
        print("- Total nodes connected to     : %d" % len(self.nodes_outbound))

    def delete_closed_connections(self):
        for n in self.nodes_inbound:
            if n.terminate_flag.is_set():
                self.inbound_node_disconnected(n)
                n.join()
                del self.nodes_inbound[self.nodes_inbound.index(n)]

        for n in self.nodes_outbound:
            if n.terminate_flag.is_set():
                self.outbound_node_disconnected(n)
                n.join()
                del self.nodes_outbound[self.nodes_inbound.index(n)]

    def send_to_nodes(self, data, exclude=[]):
        self.message_count_send = self.message_count_send + 1
        for n in self.nodes_inbound:
            if n in exclude:
                self.debug_print("send_to_nodes: Excluding node in sending the message")
            else:
                self.send_to_node(n, data)

        for n in self.nodes_outbound:
            if n in exclude:
                self.debug_print("Node send_to_nodes: Excluding node in sending the message")
            else:
                self.send_to_node(n, data)

    def send_to_node(self, n, data):
        self.message_count_send = self.message_count_send + 1
        self.delete_closed_connections()
        if n in self.nodes_inbound or n in self.nodes_outbound:
            try:
                n.send(data)

            except Exception as e:
                self.debug_print("Error al enviar la informacion al nodo (" + str(e) + ")")
        else:
            self.debug_print("No se encuentra al nodo, no se envio la informacion")

    def connect_with_node(self, host, port):
        if host == self.host and port == self.port:
            print("Conexion a si mismo imposible")
            return False

        for node in self.nodes_outbound:
            if node.host == host and node.port == port:
                print("connect_with_node: Already connected with this node.")
                return True

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.debug_print("connecting to %s port %s" % (host, port))
            sock.connect((host, port))

            # Basic information exchange (not secure) of the id's of the nodes!
            sock.send(self.id.encode('utf-8')) # Send my id to the connected node!
            connected_node_id = str(sock.recv(4096).decode('utf-8')) # When a node is connected, it sends it id!

            thread_client = self.create_new_connection(sock, connected_node_id, host, port)
            thread_client.start()

            self.nodes_outbound.append(thread_client)
            self.outbound_node_connected(thread_client)

        except Exception as e:
            self.debug_print("TcpServer.connect_with_node: Could not connect with node. (" + str(e) + ")")

    def disconnect_with_node(self, node):
        if node in self.nodes_outbound:
            self.node_disconnect_with_outbound_node(node)
            node.stop()
            node.join()  
            del self.nodes_outbound[self.nodes_outbound.index(node)]

        else:
            print("Node disconnect_with_node: cannot disconnect with a node with which we are not connected.")

    def stop(self):
        self.node_request_to_stop()
        self.terminate_flag.set()

    def create_new_connection(self, connection, id, host, port):
        return NodeConnection(self, connection, id, host, port)

    def run(self):
        while not self.terminate_flag.is_set():  
            try:
                self.debug_print("Conectando...")
                connection, client_address = self.sock.accept()
                
                connected_node_id = str(connection.recv(4096).decode('utf-8')) 
                connection.send(self.id.encode('utf-8')) 

                thread_client = self.create_new_connection(connection, connected_node_id, client_address[0], client_address[1])
                thread_client.start()

                self.nodes_inbound.append(thread_client)

                self.inbound_node_connected(thread_client)
                
            except socket.timeout:
                self.debug_print('Timeout en conexion')

            except Exception as e:
                raise e

            time.sleep(0.01)

        print("Deteniendo nodo...")
        for t in self.nodes_inbound:
            t.stop()

        for t in self.nodes_outbound:
            t.stop()

        time.sleep(1)

        for t in self.nodes_inbound:
            t.join()

        for t in self.nodes_outbound:
            t.join()

        self.sock.close()
        print("Node stopped")

    def outbound_node_connected(self, node):
        self.debug_print("Conectando con nodo saliente:")
        if self.callback is not None:
            self.callback("outbound_node_connected", self, node, {})

    def inbound_node_connected(self, node):
        self.debug_print("Conectando con nodo entrante")
        if self.callback is not None:
            self.callback("inbound_node_connected", self, node, {})

    def inbound_node_disconnected(self, node):
        self.debug_print("inbound_node_disconnected: " + node.id)
        if self.callback is not None:
            self.callback("inbound_node_disconnected", self, node, {})

    def outbound_node_disconnected(self, node):
        self.debug_print("outbound_node_disconnected: " + node.id)
        if self.callback is not None:
            self.callback("outbound_node_disconnected", self, node, {})

    def node_message(self, node, data):
        self.debug_print("node_message: " + node.id + ": " + str(data))
        if self.callback is not None:
            self.callback("node_message", self, node, data)

    def node_disconnect_with_outbound_node(self, node):
        self.debug_print("node wants to disconnect with oher outbound node: " + node.id)
        if self.callback is not None:
            self.callback("node_disconnect_with_outbound_node", self, node, {})

    def node_request_to_stop(self):
        self.debug_print("node is requested to stop!")
        if self.callback is not None:
            self.callback("node_request_to_stop", self, {}, {})

    def __str__(self):
        return 'Node: {}:{}'.format(self.host, self.port)

    def __repr__(self):
        return '<Node {}:{} id: {}>'.format(self.host, self.port, self.id)
