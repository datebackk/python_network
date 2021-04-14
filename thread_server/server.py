import socket
import threading

sock = socket.socket()
sock.bind(('', 9090))
print('Server started')

sock.listen(1)
print('Port listening')


def listen_client(conn):
    while True:
        data = conn.recv(1024)

        if not data:
            break

        print('Data from client accept:')

        msg = data.decode()
        conn.send(data)

        print(msg)


while True:
    conn, addr = sock.accept()
    print('Client connected')
    print(addr)
    threading.Thread(target=listen_client, args=(conn,)).start()
