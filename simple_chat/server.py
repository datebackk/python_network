import socket
import json
import threading
import sys

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 0))

clients = {}


class ChatServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = None
        self.clients = {}

    def start(self):
        self.server.bind(('', 0))
        self.port = self.server.getsockname()[1]
        print(f'Сервер чата запущен на порту: {self.port}', file=sys.stdout)

    def receive(self):
        while True:
            message, address = self.server.recvfrom(1024)

            print(message.decode())

            message = json.loads(message.decode())

            self.clients.setdefault(address, message['username'])

            if message['message'] != 'init':
                new_message = json.dumps({'username': self.clients[address], 'message': message['message']})

                for client_addr in self.clients:
                    self.server.sendto(str(new_message).encode(), client_addr)


class ProxyServer:
    def __init__(self, servers_pull):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 80
        self.serversPull = servers_pull

    def start(self):
        self.server.bind(('localhost', self.port))
        print(f'Прокси сервер запущен на порту : {self.port}', file=sys.stdout)

    def receive(self):
        while True:
            message, address = self.server.recvfrom(1024)
            message = json.loads(message.decode())
            distServer = self.serversPull[message['server']]
            self.server.sendto(str(distServer.port).encode(), address)


chatServer = ChatServer()
chatServer.start()

servers = {"chat_server": chatServer}

proxyServer = ProxyServer(servers)
proxyServer.start()

proxyServerThread = threading.Thread(target=proxyServer.receive)
proxyServerThread.start()

chatServerThread = threading.Thread(target=chatServer.receive)
chatServerThread.start()
