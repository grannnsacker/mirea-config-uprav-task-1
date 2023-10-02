from zipfile import ZipFile
from cfg import ZIP_PATH
from tree import Tree
import sys


class vshell:
    def __init__(self, path=ZIP_PATH):
        self.root_path = "root"
        self.current_path = ""
        self.file_system = Tree("root")
        self.zip_file = ZipFile(path)
        self.files = self.zip_file.filelist
        for i in self.files:
            print(i.filename)
        print()

    def create_file_system(self):
        for file in self.files:
            path = ["root"] + file.filename.split('/')
            path = list(filter(None, path))
            full_path = ""
            for i in range(len(path)-1):
                full_path += path[i] + '/'
                elem = self.file_system.get_node_by_path(full_path[:-1])
                if elem:
                    children = self.file_system.get_node_by_path(full_path + path[i+1])
                    if not children:
                        self.file_system.add_node(full_path[:-1], path[i+1], file.is_dir())
                else:
                    self.file_system.add_node(full_path[:-1], path[i], file.is_dir())


    def delete_last_slesh_symbol(self, path):
        if path == '' or not path or path == '/' or path[-1] != '/':
            pass
        else:
            path = path[:-1]
        return path

    def cd(self, initial_path):
        path = self.delete_last_slesh_symbol(initial_path)
        if path[0] == '/':
            # Абсолютный путь
            if path == '/':
                # Обработка cd /
                self.current_path = ""
            elif self.file_system.get_node_by_path(self.root_path + path):
                # Обработка cd {абсолютный путь}
                if self.file_system.get_node_by_path(self.root_path + path).is_directory:
                    self.current_path = path
                else:
                    print(f"\033[31mcd: can't cd to {initial_path}: Not a directory\033[0m")
            else:
                print(f"\033[31mcd: can't cd to {initial_path}: No such file or directory\033[0m")
        elif path == '..':
            # Обработка cd ..
            self.current_path = '/'.join(self.current_path.split('/')[:-1])
        else:
            # Относительный путь
            if self.file_system.get_node_by_path(self.root_path + self.current_path + '/' + path):
                if self.file_system.get_node_by_path(self.root_path + self.current_path + '/' + path).is_directory:
                    self.current_path = self.current_path + '/' + path
                else:
                    print(f"\033[31mcd: can't cd to {initial_path}: Not a directory\033[0m")

            else:
                print(f"\033[31mcd: can't cd to {initial_path}: No such file or directory\033[0m")

    def ls(self, initial_path=None):
        path = self.delete_last_slesh_symbol(initial_path)
        if not path:
            for i in self.file_system.get_node_by_path(self.root_path + self.current_path).children:
                tmp = i.path.split('/')[-1]
                print(f"\033[34m{tmp}\033[0m") if i.is_directory else print(f"\033[33m{tmp}\033[0m")
        elif path[0] == '/':
            # Абсолютный путь
            if path == '/':
                # Обработка ls /
                for i in self.file_system.get_node_by_path("root").children:
                    print(i.path.split('/')[-1])
            elif self.file_system.get_node_by_path(self.root_path + path):
                # Обработка ls {абсолютный путь}
                if self.file_system.get_node_by_path(self.root_path + path).is_directory:
                    for i in self.file_system.get_node_by_path(self.root_path + path).children:
                        tmp = i.path.split('/')[-1]
                        print(f"\033[34m{tmp}\033[0m") if i.is_directory else print(f"\033[33m{tmp}\033[0m")
                else:
                    if initial_path[-1] == '/':
                        print(f"\033[31mls: {initial_path}: Not a directory\033[0m")
                    else:
                        print(f"\033[33m{path}\033[0m")
            else:
                print(f"\033[31mls: {initial_path}: No such file or directory\033[0m")
        elif path == '..':
            # Обработка ls ..
            current_path = '/'.join(self.current_path.split('/')[:-1])
            for i in self.file_system.get_node_by_path(self.root_path + current_path).children:
                print(i.path.split('/')[-1])
        else:
            # Относительный путь
            if self.file_system.get_node_by_path(self.root_path + self.current_path + '/' + path):
                if self.file_system.get_node_by_path(self.root_path + self.current_path + '/' + path).is_directory:
                    current_path = self.current_path + '/' + path
                    for i in self.file_system.get_node_by_path(self.root_path + current_path).children:
                        tmp = i.path.split('/')[-1]
                        print(f"\033[34m{tmp}\033[0m") if i.is_directory else print(f"\033[33m{tmp}\033[0m")
                else:
                    if initial_path[-1] == '/':
                        print(f"\033[31mls: {initial_path}: Not a directory\033[0m")
                    else:
                        print(f"\033[33m{path}\033[0m")
            else:
                print(f"\033[31mls: {initial_path}: No such file or directory\033[0m")

    def pwd(self):
        text = self.root_path + ('/' if not self.current_path else self.current_path)
        print(f"\t\033[32m{text}\033[0m")

    def cat(self, initial_path=None):
        path = self.delete_last_slesh_symbol(initial_path)
        if not path:
            inp = input()
            try:
                while inp != '^C':
                    print(inp)
                    inp = input()
            except KeyboardInterrupt:
                return

        elif path == '..' or path == '/':
            # Обработка ls ..
            print("cat: read error: Is a directory")
        elif path[0] == '/':
            # Абсолютный путь
            if self.file_system.get_node_by_path(self.root_path + path):
                # Обработка ls {абсолютный путь}
                if self.file_system.get_node_by_path(self.root_path + path).is_directory:
                    print(f"\033[31mcat: read error: Is a directory\033[0m")
                else:
                    if initial_path[-1] == '/':
                        print(f"\033[31mcat: can't open {initial_path}': Not a directory\033[0m")
                    else:
                        for file in self.zip_file.filelist:
                            if path.lstrip('/') in file.filename:
                                with self.zip_file.open(file.filename, 'r') as f:
                                    for line in f.readlines():
                                        print(line.decode('utf8').strip())
            else:
                print(f"\033[31mcat: can't open '{initial_path}': No such file or directory\033[0m")
        else:
            # Относительный путь
            if self.file_system.get_node_by_path(self.root_path + self.current_path + '/' + path):
                if self.file_system.get_node_by_path(self.root_path + self.current_path + '/' + path).is_directory:
                    print(f"\033[31mcat: read error: Is a directory\033[0m")
                else:
                    if initial_path[-1] == '/':
                        print(f"\033[31mcat: can't open {initial_path}': Not a directory\033[0m")
                    else:
                        for file in self.zip_file.filelist:
                            if path in file.filename:
                                with self.zip_file.open(file.filename, 'r') as f:
                                    for line in f.readlines():
                                        print(line.decode('utf8').strip())
            else:
                print(f"\033[31mcat: can't open '{initial_path}': No such file or directory\033[0m")

    def script(self, initial_path):
        path = self.delete_last_slesh_symbol(initial_path)
        if path == '..' or path == '/':
            # Обработка ls ..
            print("script: run error: Is a directory")
        elif path[0] == '/':
            # Абсолютный путь
            if self.file_system.get_node_by_path(self.root_path + path):
                # Обработка ls {абсолютный путь}
                if self.file_system.get_node_by_path(self.root_path + path).is_directory:
                    print(f"\033[31mscript: run error: Is a directory\033[0m")
                else:
                    if initial_path[-1] == '/':
                        print(f"\033[31mscript: can't run {initial_path}': Not a directory\033[0m")
                    else:
                        for file in self.zip_file.filelist:
                            if path in file.filename:
                                with self.zip_file.open(file.filename, 'r') as f:
                                    for line in f.readlines():
                                        self.process_command(line.decode('utf8').strip())
            else:
                print(f"\033[31mscript: can't run '{initial_path}': No such file or directory\033[0m")
        else:
            # Относительный путь
            if self.file_system.get_node_by_path(self.root_path + self.current_path + '/' + path):
                if self.file_system.get_node_by_path(self.root_path + self.current_path + '/' + path).is_directory:
                    print(f"\033[31mscript: run error: Is a directory\033[0m")
                else:
                    if initial_path[-1] == '/':
                        print(f"\033[31mscript: can't run {initial_path}': Not a directory\033[0m")
                    else:
                        for file in self.zip_file.filelist:
                            if path in file.filename:
                                with self.zip_file.open(file.filename, 'r') as f:
                                    for line in f.readlines():
                                        self.process_command(line.decode('utf8').strip())
            else:
                print(f"\033[31mscript: can't run '{initial_path}': No such file or directory\033[0m")

    def process_command(self, command):
        command = command.split(" ")
        if command[0] == "pwd":
            self.pwd()
        elif command[0] == "ls":
            try:
                self.ls(command[1])
            except IndexError:
                self.ls()
        elif command[0] == "cd":
            try:
                self.cd(command[1])
            except IndexError:
                self.current_path = ""
        elif command[0] == "cat":
            try:
                self.cat(command[1])
            except IndexError:
                self.cat()
        else:
            print(f"\033[31msh: {command[0]}: not found\033[0m")

    def run(self):
        command = input(self.root_path + "/> ")
        while command != "exit":
            command = command.split(" ")
            if command[0] == '--script':
                self.script(command[1])
            elif command[0] == "pwd":
                self.pwd()
            elif command[0] == "ls":
                try:
                    self.ls(command[1])
                except IndexError:
                    self.ls()
            elif command[0] == "cd":
                try:
                    self.cd(command[1])
                except IndexError:
                    self.current_path = ""
            elif command[0] == "cat":
                try:
                    self.cat(command[1])
                except IndexError:
                    self.cat()
            else:
                print(f"\033[31msh: {command[0]}: not found\033[0m")
            command = input(self.root_path + ("/" if not self.current_path else self.current_path) + "> ")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        shell = vshell(sys.argv[1])
    else:
        shell = vshell()
    shell.create_file_system()
    shell.run()

