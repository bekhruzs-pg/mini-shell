import re
import os

class Security:
    def __init__(self):
        self.SAFE_DIR = "outputs"
        self.FILENAME_RE = r"^[a-zA-Z0-9_.\-]+$"
        self.SANDBOX_PATH = os.path.expanduser("~")
        self.ALLOWED_BUILTINS = ["ls", "dir", "echo", "pwd", "stat", "head", "tail", "cat", "cd"]

        os.makedirs(self.SAFE_DIR, exist_ok=True)

    def filename_check(self, filename: str):
        if re.match(self.FILENAME_RE, filename):
            return True
        else:
            raise ValueError(f"Invalid filename {filename}. Examples: [output123, output_123, output-123]")

    def get_safe_path(self, filename):
        return os.path.abspath(os.path.join(self.SAFE_DIR, filename))
    
    def check_path_safety(self, commands):
        args = commands[1:]
        
        for arg in args:
            path = os.path.realpath(os.path.join(os.getcwd(), arg))
            if not path.startswith(self.SANDBOX_PATH):
                raise PermissionError("You don't have permission to enter!")
            