from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    server.register_function(pow)

    def adder_function(x, y):
        return x + y

    def suma(a, b):
        return a + b
    
    def resta(a, b):
        return a - b
    
    def multiplicacion(a, b):
        return a * b
    
    def division(a, b):
        return a / b

    server.register_function(suma, 'suma')
    server.register_function(resta, 'resta')
    server.register_function(multiplicacion, 'multiplicacion')
    server.register_function(division, 'division')

    server.serve_forever()