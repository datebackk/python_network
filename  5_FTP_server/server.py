import os
import shutil
import socket
import subprocess
import sys

if sys.platform == 'win32':
    separator = '\\'
else:
    separator = '/'

try:
    os.mkdir(os.getcwd() + separator + 'home')
except:
    print('Файл уже существует')


class FileManager:
    def __init__(self):
        self.history = []
        self.pwd = os.getcwd() + separator + 'home' + separator
        self.minPath = self.pwd

    def path_exist(self, path):
        # if os.path.exists(path) and len(self.minPath) <= len(os.path.abspath(path)):
        if os.path.exists(path):
            return os.path.exists(path)
        else:
            print('Путь не существует')
            return os.path.exists(path)

    def mkdir(self, path):
        if len(path.split(separator)) > 2:
            os.makedirs(self.pwd + path)
        else:
            os.mkdir(self.pwd + path)

    def ls(self):
        print(os.listdir(self.pwd))

    def touch(self, path_to_file):
        file = open(self.pwd + path_to_file, "w+")
        file.close()

    def cd(self, path):
        if os.path.isdir(os.path.abspath(self.pwd + path)):
            if path == '..':
                if len(self.history) != 0:
                    self.pwd = self.history[-1]
                    del self.history[-1]
                else:
                    print('Выше подняться нельзя')
            else:
                self.history.append(self.pwd)
                self.pwd = os.path.abspath(self.pwd + path) + separator
        else:
            print('Не дериктория')

    def cat(self, path):
        if os.path.isfile(self.pwd + path):
            file = open(self.pwd + path, "r")
            for i, line in enumerate(file.readlines()):
                print(line[:-1])
        else:
            print('Не файл')

    def mv(self, path, pathTo):
        path = self.pwd + path
        pathTo = self.pwd + pathTo
        try:
            shutil.move(path, pathTo)
        except:
            print('Проверьте пути')

    def open(self, path):
        if os.path.isfile(self.pwd + path):
            if sys.platform == 'win32':
                os.startfile(self.pwd + path)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, self.pwd + path])
        else:
            print('Не файл')

    def cp(self, path, pathTo):
        path = self.pwd + path
        pathTo = self.pwd + pathTo

        if os.path.isfile(path):
            if os.path.isdir(pathTo):
                shutil.copy2(path, pathTo)
            else:
                print('Путь назначения не является директорией')
        else:
            print('Вы копируете не файл')

    def rm(self, path):
        path = self.pwd + path

        if os.path.isfile(path):
            os.remove(path)
            return

        if os.path.isdir(path):
            shutil.rmtree(path)
            return

    def commands_handler(self, line):
        event = line.split(' ')[0]
        try:
            param = line.split(' ')[1]
        except:
            pass

        try:
            param2 = line.split(' ')[2]
        except:
            pass

        if event == 'mkdir':
            self.mkdir(param)
            return

        if event == 'ls':
            self.ls()
            return

        if event == 'cd':
            if self.path_exist(self.pwd + param):
                self.cd(param)
            return

        if event == 'touch':
            self.touch(param)
            return

        if event == 'cat':
            if self.path_exist(self.pwd + param):
                self.cat(param)
            return

        if event == 'cp':
            if self.path_exist(self.pwd + param):
                self.cp(param, param2)
            return

        if event == 'mv':
            self.mv(param, param2)
            return

        if event == 'open':
            if self.path_exist(self.pwd + param):
                self.open(param)
            return

        if event == 'rm':
            if self.path_exist(self.pwd + param):
                self.rm(param)
            return

        print('Команда не существует')


fileManager = FileManager()

sock = socket.socket()
sock.bind(('', 9090))
print('Server started')

sock.listen(1)

while True:
    conn, addr = sock.accept()
    print('Client connected')
    print(addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break

        msg = data.decode()

        fileManager.commands_handler(msg)

        conn.send(fileManager.pwd.encode())
