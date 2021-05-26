import socket

sock = socket.socket()
sock.setblocking(True)
sock.connect(('localhost', 9090))
print('Connected to server')
path = '5_FTP_server\home\ '
while True:

    msg = input(path)

    if msg == 'exit':
        sock.close()
        print('Disconnected from server')
        break

    sock.send(msg.encode())

    data = sock.recv(1024)

    path = data.decode()

    # print(data.decode())