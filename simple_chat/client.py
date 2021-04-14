import json
import socket
import threading


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(True)
sock.connect(('localhost', 80))


msg = json.dumps({'server': 'chat_server'})
sock.send(str(msg).encode())
dist_port = int((sock.recv(1024)).decode())
sock.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(True)
sock.connect(('localhost', dist_port))
print(f'Connected to server')

username = input('Введите имя пользователя: ')
msg = json.dumps({'username': username, 'message': 'init'})
sock.send(str(msg).encode())

with open('history.txt', 'r') as f:
    messages = f.read().splitlines()

for message in messages:
    print(message)
print('Новые сообщения')


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