import http.server
import socketserver
import datetime
import os
import os.path
from io import BytesIO
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("\nMethod GET")
        if self.path == '/':
            self.path = 'home.html'
        print("Regresando home.html")
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        print("\nMethod POST")
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        print("Regresando parametros recibidos")
        return self.wfile.write(response.getvalue())

    def do_PUT(self):
        print("\nMethod PUT")
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is PUT request. ')
        response.write(b'Received: ')
        response.write(body)
        print("creando archivo " + body.decode())
        archivo = open(body.decode(), "w")
        archivo.write("Hola")
        archivo.close()
        archivo = open(body.decode()+"respaldo", "w")
        archivo.write("Hola respaldo")
        archivo.close()        
        return self.wfile.write(response.getvalue())
    
    def do_DELETE(self):
        print("\nMethod DELETE")
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is DELETE request. ')
        response.write(b'Received: ')
        response.write(body)
        os.remove(body.decode())
        print("Borrando archivo :" + body.decode())
        return self.wfile.write(response.getvalue())

    def do_CONNECT(self):
        print("\nMethod CONNECT")
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is CONNECT request. ')
        response.write(b'Received: ')
        response.write(body)
        print("Conectando con: " + body.decode())
        conn = http.client.HTTPConnection("127.0.0.1:8000")
        print(conn)
        print("Conectado")
        return self.wfile.write(response.getvalue())
    
    def do_OPTIONS(self):
        print("\nMethod OPTIONS")
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        print("Generando opciones disponibles")
        response.write(b'This is Option server request. ')
        response.write(body)
        response.write(("\n" + str(datetime.datetime.now())).encode())
        response.write("\nGET POST PUT DELETE CONNECT OPTIONS are allowed method".encode())
        return self.wfile.write(response.getvalue())

    def do_TRACE(self):
        print("\nMethod TRACE")
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        print("Buscando archivo: " + body.decode())
        response.write(b'This is Trace server request. ')
        response.write(body)        
        response.write(("\nfile " + body.decode() + " exist: " +  str(os.path.isfile(body.decode()))).encode())
        return self.wfile.write(response.getvalue())

handler_object = MyHttpRequestHandler

PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)
my_server.serve_forever()
