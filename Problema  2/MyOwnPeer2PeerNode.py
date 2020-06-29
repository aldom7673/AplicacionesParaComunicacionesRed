from node import Node

class MyOwnPeer2PeerNode (Node):

    # Python class constructor
    def __init__(self, host, port):
        super(MyOwnPeer2PeerNode, self).__init__(host, port, None)
        print("Iniciando...")

    # all the methods below are called when things happen in the network.
    # implement your network node behavior to create the required functionality.

    def outbound_node_connected(self, node):
        print("Conectando con nodo saliente")
        
    def inbound_node_connected(self, node):
        print("Conectando con nodo entrante")

    def inbound_node_disconnected(self, node):
        print("Desconectado con nodo entrante")

    def outbound_node_disconnected(self, node):
        print("Desconectado con nodo saliente")

    def node_message(self, node, data):
        print("Mensaje nuevo de " + str(data))
        
    def node_disconnect_with_outbound_node(self, node):
        print("El nodo se desconetará del nodo")
        
    def node_request_to_stop(self):
        print("El nodo se dentendra")
        
