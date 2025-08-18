import readline
from command_handler import CommandHandler
import os

HISTFILE = os.path.expanduser("~/.mysh_history")

if os.path.exists(HISTFILE):
    readline.read_history_file(HISTFILE)

readline.set_completer()

if __name__ == "__main__":
    handler = CommandHandler()
    while True:
        command, commands = handler.command_field()
        if not command:
            continue

        if ">" in command:
            print(handler.output_file(command))

        match commands[0]:
            case "exit":
                break
            case "ls":
                handler.get_ls(commands)
            case "pwd":
                print(handler.get_pwd())
            case "cd":
                print(handler.chdir_handle(command))
            case ("clear" | "cls"):
                handler.clear_cmdhist()
            case "echo":
                print(handler.handle_echo(commands))
            case "export":
                print(handler.handle_export(commands))
            case "mkdir":
                print(handler.handle_mkdir(commands))
            case "rmdir":
                print(handler.handle_rmdir(commands))
            case _:
                print(handler.handle_others(commands))
    
    readline.write_history_file(HISTFILE)