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
        chatHistory = open("log.txt", "a+")
        chatHistory.writelines([f'{data} \n'])
        chatHistory.flush()
        chatHistory.close()

        conn.send(data)

        print(msg)


def conn_accept(stop, stop1):
    while not stop:
        conn, addr = sock.accept()
        print('Client connected')
        print(addr)
        threading.Thread(target=listen_client, args=(conn,)).start()


def pause():
    while True:
        print('pause')


cannAccept = threading.Thread(target=conn_accept, args=[False, False]).start()
