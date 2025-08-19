import readline
from command_handler import CommandHandler, Command
import os

HISTFILE = os.path.expanduser("~/.mysh_history")

if os.path.exists(HISTFILE):
    readline.read_history_file(HISTFILE)

readline.set_completer()
readline.set_history_length(1000)

command_count = 0

if __name__ == "__main__":
    handler = CommandHandler()
    while command_count<1000:
        command_count += 1
        command, commands = handler.command_field()

        if len(command)>=1000:
            print("[-] Too much commad length! Must be bellow 1000 letters.")
            continue

        if not command:
            continue

        if ">" in command:
            print(handler.output_file(command))
            continue

        if commands[0] == "exit":
            print("See, ya)")
            break

        print(Command(command, commands).get_output())

    readline.write_history_file(HISTFILE)

if command_count>=1000:
    print("You used too many commmands, we need to shoutdown the shell!")