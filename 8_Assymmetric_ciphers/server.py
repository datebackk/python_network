import socket
import threading
import uuid
import json
from encryptor import Encryptor
from test import database

class AuthServer:
    def __init__(self):
        self.address = ('', 9090)
        self.sock = socket.socket()
        self.clients = dict()
        self.p = 7
        self.g = 5
        self.privateKey = database.getServerPrivateKey()
        self.publicKey = database.getServerPublicKey(self.p ** self.privateKey % self.g)
        self.allowedKeys = [1, 2, 5, 6, 7, 8, 10, 11, 13, 15, 16, 19]

    def start(self):
        self.sock.bind(self.address)
        self.sock.listen()

    def receive(self):
        while True:
            conn, addr = self.sock.accept()
            print('Client connected')
            print(addr)
            while True:
                data = conn.recv(1024)
                newUUID = str(uuid.uuid4())

                if int(data.decode()) not in self.allowedKeys:
                    print('попал')
                    conn.send(json.dumps({'uuid': -1, 'msg': '-1'}).encode())
                    conn.close()
                    break

                self.clients.setdefault(newUUID, int(data.decode()))
                print(f'Key from client accept: {data.decode()}')
                msg = json.dumps({'uuid': newUUID, 'msg': self.publicKey}).encode()
                conn.send(msg)
                conn.close()
                break


class MessageServer:
    def __init__(self):
        self.address = ('', 9091)
        self.sock = socket.socket()

    def start(self):
        self.sock.bind(self.address)
        self.sock.listen()

    def receive(self):
        while True:
            conn, addr = self.sock.accept()
            print('Client connected')
            print(addr)
            while True:
                data = conn.recv(1024)

                data = json.loads(data.decode())
                clientPubKey = authSever.clients[data['uuid']]
                print(f'Data from client encrypt: {data["msg"]}')

                msg = Encryptor.decrypt(data["msg"], clientPubKey ** authSever.privateKey % authSever.g)
                print(f'Data from client decrypt: {msg}')
                conn.send(data['msg'].encode())


authSever = AuthServer()
messageServer = MessageServer()

authSever.start()
messageServer.start()

authSeverThread = threading.Thread(target=authSever.receive)
authSeverThread.start()

messageServerThread = threading.Thread(target=messageServer.receive)
messageServerThread.start()
