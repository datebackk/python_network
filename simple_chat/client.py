import json
import socket
import sys
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(True)
sock.connect(('localhost', 9090))
print('Connected to server')

username = input('Enter yor username: ')


def receive():
    while True:
        data = sock.recv(1024)
        incoming_message = json.loads(data.decode())

        if incoming_message['username'] != username:
            print(incoming_message['username'] + ' -> ' + incoming_message['message'])


def write():
    while True:
        msg = input()
        if msg == 'exit':
            sock.close()
            print('Disconnected from server')
            break
        msg = json.dumps({'username': username, 'message': msg})
        sock.send(str(msg).encode())


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()