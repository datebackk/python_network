import socket
from multiprocessing import Process


def check_ports(mod, mod1):
    openedPorts = []
    for port in range(mod, 65, 2):
        try:
            sock = socket.socket()
            sock.bind(('localhost', port))
        except OSError:
            continue
        openedPorts.append(port)
    print(openedPorts)


openedPorts1 = Process(target=check_ports, args=(2, 2)).run()
openedPorts2 = Process(target=check_ports, args=(3, 3)).run()
