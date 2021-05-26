import datetime
import socket
import threading

UTF = 'utf-8'


def start():
    with open('settings.txt', 'r') as f:
        settings = f.read().split('\n')
        port = int(settings[0].split(':')[1])
        listen = int(settings[1].split(':')[1])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', port))
    server.listen(listen)

    while True:
        client, address = server.accept()
        data = client.recv(1024)

        try:
            data = data.decode(UTF)
        except:
            try:
                data = data.replace('"', "")
            except:
                pass

        log = open("log.txt", "a+")
        try:
            log.writelines([f'Path: {data.split(" ")[1]} Time: {datetime.datetime.now()} Address: {address} \n'])
            log.flush()
            log.close()
        except IndexError:
            log.writelines([f'Time: {datetime.datetime.now()} Address: {address} \n'])
            log.flush()
            log.close()
            client.shutdown(socket.SHUT_WR)

        content = get_route(data)
        client.send(content)

        client.shutdown(socket.SHUT_WR)


def get_route(request):
    Status = f'HTTP/1.1 200 OK\r\n'
    Date = f'Date: {datetime.datetime.now()}\r\n'
    Connection = 'Connection: close\r\n'
    ContentLength = 'Content-length: '
    Server = 'Server: MyServer\r\n\r\n'
    ContentType = f'Content-Type: text/html; charset={UTF}\r\n'

    ForbiddenExtensions = ['js', 'css']

    try:
        path = request.split(' ')[1]
    except IndexError:
        return "error".encode(UTF)
    page = None

    if path == '/':
        page = '/index.html'
    elif path == '/image':
        ContentType = 'Content-Type: image/png'
        page = '/python.png'
    elif path == '/protected':
        page = '/403.html'
    else:
        try:
            extension = path.split('.')[1]
            if extension in ForbiddenExtensions:
                page = '/403.html'
            else:
                page = '/404.html'
        except IndexError:
            page = '/404.html'

    response = ''
    with open('pages' + page, 'rb') as file:
        response = file.read()
    ContentLength += str(len(response)) + '\r\n'
    HEADERS = Status + Connection + ContentLength + ContentType + Date + Server
    return HEADERS.encode(UTF) + response


Server = threading.Thread(target=start).start()
