import http.client
import urllib.parse
import json
import time

REMOTE_SERVER_HOST = 'localhost:8000'
REMOTE_SERVER_PATH = '/'

print("\nGET")
conn = http.client.HTTPConnection(REMOTE_SERVER_HOST)
conn.request("GET", "/")
r1 = conn.getresponse()
print(r1.status, r1.reason)
data1 = r1.read()
print(data1)
time.sleep(3)

print("\nHEAD")
conn.request("HEAD", "/")
r1 = conn.getresponse()
print(r1.status, r1.reason)
data1 = r1.read()
print(r1.getheaders())
print(data1)
time.sleep(3)

print("\nPOST")
params = urllib.parse.urlencode({'nombre': 'aldo', 'metodo': 'POST'})
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn.request("POST", "", params, headers)
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
print(data.decode())
time.sleep(3)

print("\nPUT")
BODY = "archivo.txt"
conn.request("PUT", "/file", BODY)
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
print(data.decode())
time.sleep(3)

print("\nDELETE")
conn.request("DELETE", "/file", "archivo.txt")
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
print(data.decode())
time.sleep(3)

print("\nCONNECT")
conn.request("CONNECT", "/host", "127.0.0.1")
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
print(data.decode())
time.sleep(3)

print("\nOPTIONS")
conn.request("OPTIONS", "*", "localhost")
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
print(data.decode())
time.sleep(3)

print("\nTRACE")
conn.request("TRACE", "/file", "archivo.txt")
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
print(data.decode())
time.sleep(3)
