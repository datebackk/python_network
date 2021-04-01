import json
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(True)
sock.connect(('localhost', 80))


while True:
    msg = json.dumps({'server': 'chat_server'})
    sock.send(str(msg).encode())

    data = sock.recv(1024)
    print(data.decode())
