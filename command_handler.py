import subprocess as sp
import os

class CommandHandler:
    def __init__(self):
        if os.name == "nt":  # Windows
            self.ls_cmd, self.clear_cmd = "dir", "cls"
            self.home, self.user = "USERPROFILE", "USERNAME"
        else:
            self.ls_cmd, self.clear_cmd = "ls", "clear"
            self.home, self.user = "HOME", "USER"
        
    def command_field(self):
        prompt = os.path.basename(os.getcwd())
        command = input(f"[{prompt}] mysh> ")
        commands = command.split()

        return [command, commands]
    
    def output_file(self, command):
        new_command, filename = command.split(">") 
        new_command, filename = new_command.strip(), filename.strip()
        with open(filename, "w") as file:
            sp.Popen(new_command, stdout=file, shell=True).communicate()
        return f"Output has written to {filename}!"
    
    def get_ls(self, commands: list):
        if len(commands) == 1:
                sp.run(self.ls_cmd, shell=True)
        else:
            sp.run(f"{self.ls_cmd} {commands[1]}", shell=True)

    def get_pwd(self):
        return os.getcwd()    

    def chdir_handle(self, command):
        commands = command.split(" ", 1)
        cd_path = commands[1].replace("\"", "") if "\"" in commands[1] else commands[1] 
        try:
            os.chdir(cd_path)
            return os.getcwd()
        except IndexError:
            cur_path = os.getcwd()
            return f"Current path: {cur_path}"
        except FileNotFoundError:
            return f"cd: no such file or directory: {cd_path}"
        except OSError:
            return f"cd: no such file or directory: {cd_path}"
    def clear_cmdhist(self):
        os.system(self.clear_cmd)
    def handle_echo(self, commands):
        if commands[1] == "$HOME":
            return os.environ.get(self.home)
        elif commands[1] == "$USER":
            return os.environ.get(self.user)
        elif commands[1][0] == "$":
            return os.environ.get(commands[1][1:])
        else:
            return " ".join(commands[1:])
    def handle_export(self, commands):
        try:
            key, value = commands[1].split("=")
            os.environ[key] = value
            return f"New key added: {key}={value}"
        except:
            return "Invalid key or command. Sample: [export KEY=VALUE]"
    def handle_mkdir(self, commands):
        try:
            path = " ".join(commands[1:]).replace("\"", "") if "\"" in " ".join(commands[1:]) else commands[1:] 
            os.mkdir(path)
            return f"New folder created! [{os.getcwd()}\\{path}]"
        except OSError:
            return f"Folder name syntax is incorrect: {path}"
    def handle_rmdir(self, commands):
        try:
            path = " ".join(commands[1:]).replace("\"", "") if "\"" in " ".join(commands[1:]) else commands[1:] 
            os.rmdir(path)
            return f"Folder deleted! [{os.getcwd()}\\{path}]"
        except OSError:
            return f"Folder name syntax is incorrect: {path}"
    def handle_others(self, commands):
        output = sp.run(" ".join(commands) if len(commands) > 1 else commands[0], capture_output=True, text=True, shell=True)
        return output.stdout