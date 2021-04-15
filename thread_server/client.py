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
    elif msg == 'log':
        with open('log.txt', 'r') as f:
            messages = f.read().splitlines()

        for message in messages:
            print(message)
    elif msg == 'clear-log':
        with open('log.txt', 'w+') as f:
            f.write(' ')

    sock.send(msg.encode())
    print('Data send to server')

    data = sock.recv(1024)
    print('Data recive from server:')

    print(data.decode())
