import subprocess as sp
import shlex
from security import Security
import os

class Command:
    def __init__(self, command, commands):
        handler = CommandHandler()
        self.output = ""
        match commands[0]:
            case "ls":
                self.output = handler.get_ls(commands)
            case "pwd":
                self.output = handler.get_pwd()
            case "cd":
                self.output = handler.chdir_handle(command)
            case ("clear" | "cls"):
                handler.clear_cmdhist()
                self.output = "[#] Mini-Shell - Made by Bekhruz!"
            case "echo":
                self.output = handler.handle_echo(commands)
            case "export":
                self.output = handler.handle_export(commands)
            case "mkdir":
                self.output = handler.handle_mkdir(commands)
            case "rmdir":
                self.output = handler.handle_rmdir(commands)
            case _:
                output = handler.handle_others(commands)
                self.output = output[0] if output[0] else output[1]
    def get_output(self):
        return self.output

class CommandHandler:
    def __init__(self):
        self.security = Security()
        if os.name == "nt":  # Windows
            self.ls_cmd, self.clear_cmd = "dir", "cls"
            self.home, self.user = "USERPROFILE", "USERNAME"
        else:
            self.ls_cmd, self.clear_cmd = "ls", "clear"
            self.home, self.user = "HOME", "USER"
        
    def command_field(self):
        prompt = os.path.basename(os.getcwd())
        command = input(f"[{prompt}] mysh> ")
        commands = shlex.split(command)
        self.security.check_path_safety(commands)

        return [command, commands]
    
    def output_file(self, command):
        new_command, filename = command.split(">", 1)
        new_command, filename = new_command.strip(), filename.strip()
        try:
            if self.security.filename_check(filename):
                output_path = self.security.get_safe_path(filename)
                commands = shlex.split(command)
                fd = os.open(output_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 600)
                with os.fdopen(fd, "w", encoding="utf-8") as file:
                    file.write(Command(new_command, shlex.split(new_command)).get_output())
                return f"[+] Output has written to [{output_path}]!"
        except ValueError as e:
            return f"[-] {e.args[0]}"
    
    def get_ls(self, commands: list):
        if len(commands) == 1:
            output = sp.run(self.ls_cmd, capture_output=True, text=True, shell=True)
            return output.stdout
        else:
            output = sp.run(f"{self.ls_cmd} {commands[1]}", capture_output=True, text=True, shell=True)
            return output.stdout

    def get_pwd(self):
        return f"[/] {os.getcwd()}"

    def chdir_handle(self, command):
        commands = command.split(" ", 1)
        cd_path = ""
        try:
            cd_path = commands[1].replace("\"", "") if "\"" in commands[1] else commands[1] 
            os.chdir(cd_path)
            return f"[/] {os.getcwd()}"
        except IndexError:
            cur_path = os.getcwd()
            return f"[/] Current path: {cur_path}"
        except FileNotFoundError:
            return f"[-] cd: no such file or directory: {cd_path}"
        except OSError:
            return f"[-] cd: no such file or directory: {cd_path}"
    def clear_cmdhist(self):
        os.system(self.clear_cmd)
    def handle_echo(self, commands):
        if len(commands) > 1:    
            if commands[1] == "$HOME":
                return os.environ.get(self.home)
            elif commands[1] == "$USER":
                return os.environ.get(self.user)
            elif commands[1][0] == "$":
                return os.environ.get(commands[1][1:])
            else:
                return " ".join(commands[1:])
        else:
            return ""
    def handle_export(self, commands):
        try:
            key, value = commands[1].split("=")
            os.environ[key] = value
            return f"[+] New key added: {key}={value}"
        except:
            return "[-] Invalid key or command. Sample: [export KEY=VALUE]"
    def handle_mkdir(self, commands):
        try:
            path = " ".join(commands[1:]).replace("\"", "") if "\"" in " ".join(commands[1:]) else " ".join(commands[1:]) 
            os.mkdir(path)
            return f"[+] New folder created! [{os.getcwd()}\\{path}]"
        except OSError:
            return f"[-] Folder name syntax is incorrect: {path}"
    def handle_rmdir(self, commands):
        try:
            path = " ".join(commands[1:]).replace("\"", "") if "\"" in " ".join(commands[1:]) else " ".join(commands[1:]) 
            os.rmdir(path)
            return f"[+] Folder deleted! [{os.getcwd()}\\{path}]"
        except OSError:
            return f"[-] Folder name syntax is incorrect: {path}"
    def handle_others(self, commands):
        try:
            if commands[0] in self.security.ALLOWED_BUILTINS:
                output = sp.run(" ".join(commands) if len(commands) > 1 else commands[0], capture_output=True, text=True, shell=True)
            else:
                output = sp.run(commands, capture_output=True, text=True, shell=False)
        except FileNotFoundError:
            return f"[-] There is no command named {commands[0]}"

        return output.stdout, output.stderr