import os
import sys
import subprocess as sp
import shlex
import re
from pathlib import Path
import string

# ----- History setup (readline optional) -----
HISTFILE = Path.home() / ".mysh_history"
_readline = None
try:
    import readline as _readline
    if HISTFILE.exists():
        _readline.read_history_file(str(HISTFILE))
except Exception:
    _readline = None  # Windows or unavailable; continue without history

def save_history():
    if _readline:
        try:
            # Ensure parent exists
            HISTFILE.parent.mkdir(parents=True, exist_ok=True)
            _readline.write_history_file(str(HISTFILE))
        except Exception:
            pass

# ----- Helpers -----
IS_WINDOWS = os.name == "nt"

def sanitize_env_var_name(name: str) -> str:
    """Sanitize environment variable name to prevent injection."""
    # Only allow alphanumeric chars and underscore
    allowed_chars = string.ascii_letters + string.digits + '_'
    return ''.join(c for c in name if c in allowed_chars)

def sanitize_path(path: str) -> str:
    """Sanitize file paths to prevent directory traversal."""
    # Resolve the path and ensure it's within safe bounds
    try:
        resolved = Path(path).resolve()
        # Check for attempts to escape current working directory tree
        cwd = Path.cwd().resolve()
        try:
            resolved.relative_to(cwd.parent)  # Allow access to parent for reasonable navigation
        except ValueError:
            # Path tries to escape too far up, restrict to home directory
            home = Path.home().resolve()
            if not str(resolved).startswith(str(home)):
                raise ValueError("Path access denied")
        return str(resolved)
    except (OSError, ValueError):
        # If path resolution fails, return the original but sanitized
        return os.path.normpath(path)

def sanitize_command(cmd: str) -> str:
    """Sanitize command names to prevent injection."""
    # Only allow alphanumeric chars, underscore, hyphen, and dot
    allowed_chars = string.ascii_letters + string.digits + '_-.'
    return ''.join(c for c in cmd if c in allowed_chars)

def validate_redirect_path(path: str) -> str:
    """Validate and sanitize file redirection paths."""
    if not path:
        raise ValueError("Empty redirect path")
    
    # Sanitize the path
    sanitized = sanitize_path(path)
    
    # Additional checks for redirection
    if '..' in path:
        raise ValueError("Directory traversal not allowed in redirects")
    
    # Ensure we're not trying to overwrite system files
    dangerous_paths = ['/etc', '/bin', '/usr/bin', '/sys', '/proc']
    if IS_WINDOWS:
        dangerous_paths.extend(['C:\\Windows', 'C:\\System32'])
    
    for dangerous in dangerous_paths:
        if sanitized.startswith(dangerous):
            raise ValueError("Cannot redirect to system directories")
    
    return sanitized

def expand_user_vars(s: str) -> str:
    """Expand ~ and $VAR with proper sanitization."""
    # Expand ~ first
    s = os.path.expanduser(s)
    
    # Replace $VAR or ${VAR} with sanitization
    def repl(m):
        var = m.group("braced") or m.group("plain")
        # Sanitize the variable name to prevent injection
        var = sanitize_env_var_name(var)
        if not var:  # If sanitization left nothing, return empty
            return ""
        return os.environ.get(var, "")
    
    return re.sub(r"\$(?:\{(?P<braced>[^}]+)\}|(?P<plain>[A-Za-z_][A-Za-z0-9_]*))", repl, s)

def builtin_ls(args):
    target = args[0] if args else "."
    target = expand_user_vars(target)
    
    # Sanitize the target path
    try:
        target = sanitize_path(target)
    except ValueError as e:
        print(f"ls: {e}")
        return
    
    try:
        entries = os.listdir(target)
        entries.sort()
        # Simple multi-column-ish output
        print("  ".join(entries))
    except FileNotFoundError:
        print(f"ls: no such file or directory: {target}")
    except NotADirectoryError:
        print(target)
    except PermissionError:
        print(f"ls: permission denied: {target}")

def builtin_cd(args):
    if not args:
        path = os.path.expanduser("~")
    else:
        path = expand_user_vars(args[0])
    
    # Sanitize the path
    try:
        path = sanitize_path(path)
    except ValueError as e:
        print(f"cd: {e}")
        return
    
    try:
        os.chdir(path)
    except FileNotFoundError:
        print(f"cd: no such file or directory: {path}")
    except NotADirectoryError:
        print(f"cd: not a directory: {path}")
    except PermissionError:
        print(f"cd: permission denied: {path}")

def builtin_pwd():
    print(os.getcwd())

def builtin_echo(args):
    if not args:
        print()
        return
    
    # Sanitize and expand each argument
    expanded = []
    for arg in args:
        try:
            expanded.append(expand_user_vars(arg))
        except Exception:
            # If expansion fails, use the original (but don't expand)
            expanded.append(arg)
    
    print(" ".join(expanded))

def builtin_export(args):
    if not args:
        # Show current env for convenience (sorted)
        for k in sorted(os.environ.keys()):
            print(f"{k}={os.environ[k]}")
        return
    
    # Accept KEY=VALUE (VALUE may be quoted)
    for item in args:
        if "=" not in item:
            print(f"export: invalid assignment: {item}")
            continue
        
        key, value = item.split("=", 1)
        key = key.strip()
        
        # Sanitize the key name
        sanitized_key = sanitize_env_var_name(key)
        if not sanitized_key:
            print(f"export: invalid variable name: {key}")
            continue
        
        # Strip surrounding quotes if present
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        
        # Expand variables in the value
        try:
            expanded_value = expand_user_vars(value)
            os.environ[sanitized_key] = expanded_value
        except Exception as e:
            print(f"export: error setting {sanitized_key}: {e}")

def builtin_clear():
    # Cross-platform clear - safer than os.system
    if IS_WINDOWS:
        os.system("cls")
    else:
        os.system("clear")

def run_external(cmd_argv, stdout=None):
    """Run external command with sanitization."""
    if not cmd_argv:
        return
    
    # Sanitize the command name
    sanitized_cmd = sanitize_command(cmd_argv[0])
    if not sanitized_cmd:
        print(f"Invalid command name: {cmd_argv[0]}")
        return
    
    # Create sanitized argv
    sanitized_argv = [sanitized_cmd] + cmd_argv[1:]
    
    try:
        sp.run(sanitized_argv, check=False, stdout=stdout)
    except FileNotFoundError:
        print(f"{sanitized_cmd}: command not found")
    except Exception as e:
        print(f"Error running {sanitized_cmd}: {e}")

# ----- Main REPL -----
def main():
    while True:
        try:
            prompt = os.path.basename(os.getcwd()) or "/"
            raw = input(f"[{prompt}] mysh> ").strip()
            if not raw:
                continue

            # Basic input validation
            if len(raw) > 1000:  # Prevent extremely long commands
                print("Command too long")
                continue

            # Parse with shlex to honor quotes
            try:
                tokens = shlex.split(raw)
            except ValueError as e:
                print(f"Parse error: {e}")
                continue

            if not tokens:
                continue

            # Built-in: exit
            if tokens[0] in ("exit", "quit"):
                break

            # Handle simple output redirection at the end: '... > file' or '... >> file'
            redirect = None
            mode = None
            if len(tokens) >= 3 and tokens[-2] in (">", ">>"):
                try:
                    redirect = validate_redirect_path(expand_user_vars(tokens[-1]))
                    mode = "a" if tokens[-2] == ">>" else "w"
                    tokens = tokens[:-2]
                except ValueError as e:
                    print(f"Redirect error: {e}")
                    continue

            if not tokens:
                continue

            cmd, *args = tokens

            # Handle built-in commands
            if cmd == "pwd":
                builtin_pwd()
                continue
            if cmd == "cd":
                builtin_cd(args)
                continue
            if cmd == "echo":
                builtin_echo(args)
                continue
            if cmd == "export":
                builtin_export(args)
                continue
            if cmd == "clear":
                builtin_clear()
                continue
            if cmd == "ls":
                builtin_ls(args)
                continue

            # External command
            # Expand ~ in args for convenience; leave env expansion to the program
            try:
                argv = [expand_user_vars(cmd)] + [expand_user_vars(a) for a in args]
            except Exception as e:
                print(f"Error expanding arguments: {e}")
                continue

            # Execute with optional redirection
            if redirect:
                try:
                    with open(redirect, mode, encoding="utf-8", newline="") as fh:
                        run_external(argv, stdout=fh)
                except Exception as e:
                    print(f"Redirect error: {e}")
            else:
                run_external(argv)

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except EOFError:
            print()
            break
        except Exception as e:
            print(f"Error: {e}")

    save_history()

if __name__ == "__main__":
    main()
