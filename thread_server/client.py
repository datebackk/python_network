import socket

sock = socket.socket()
sock.setblocking(True)
sock.connect(('localhost', 9090))
print('Connected to server')

while True:
    msg = input('Print your message: ')

    if msg == 'exit':
        sock.close()
        print('Disconnected from server')
        break

    sock.send(msg.encode())
    print('Data send to server')

    data = sock.recv(1024)
    print('Data recive from server:')

    print(data.decode())
