import json
import socket
import random
from encryptor import Encryptor


class Client:
    def __init__(self):
        self.p = 7
        self.g = 5
        self.privateKey = random.randint(1, 20)
        self.publicKey = self.p ** self.privateKey % self.g
        self.authServerKey = None
        self.messageServer = ('localhost', 9091)
        self.authServer = ('localhost', 9090)
        self.uuid = None
        self.sharedKey = None

    def get_private_key(self):
        sock = socket.socket()
        sock.connect(self.authServer)
        sock.send(str(self.publicKey).encode())
        data = sock.recv(1024)

        data = json.loads(data.decode())

        if data['uuid'] == -1:
            print('Такой публичный ключ не разрешен')
            quit(0)

        print(f'Server key received: {data["msg"]}')
        self.authServerKey = int(data["msg"])
        self.sharedKey = self.authServerKey ** self.privateKey % self.g
        self.uuid = data["uuid"]
        sock.close()

    def start_messaging(self):
        sock = socket.socket()
        sock.connect(self.messageServer)

        while True:
            msg = input('Print your message: ')

            if msg == 'exit':
                sock.close()
                print('Disconnected from server')
                break

            msg = Encryptor.encrypt(msg, self.sharedKey)
            msg = json.dumps({'uuid': self.uuid, 'msg': msg}).encode()
            sock.send(msg)
            print('Data send to server')

            data = sock.recv(1024)
            data = Encryptor.decrypt(data.decode(), self.sharedKey)
            print(f'Data receive from server: {data}')


client = Client()

client.get_private_key()

client.start_messaging()
