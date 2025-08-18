# MyShell - A Secure Python Shell Implementation

A secure, cross-platform shell implementation in Python with built-in sanitization features to prevent common security vulnerabilities.

## Features

### Security Features
- **Command Injection Prevention**: Sanitizes command names to prevent injection attacks
- **Path Traversal Protection**: Validates and sanitizes file paths to prevent directory traversal
- **Environment Variable Sanitization**: Cleanses environment variable names and values
- **Safe File Redirection**: Validates redirect paths and prevents overwriting system files
- **Input Validation**: Limits command length and validates user input

### Built-in Commands
- `pwd` - Print current working directory
- `cd [directory]` - Change directory (with ~ and $VAR expansion)
- `ls [directory]` - List directory contents
- `echo [text]` - Print text (with variable expansion)
- `export KEY=VALUE` - Set environment variables
- `clear` - Clear the terminal screen
- `exit`/`quit` - Exit the shell

### Additional Features
- **Command History**: Persistent command history (when readline is available)
- **Variable Expansion**: Support for `~` (home directory) and `$VAR`/`${VAR}` environment variables
- **Output Redirection**: Support for `>` and `>>` redirection operators
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Quoted Arguments**: Proper handling of quoted strings using `shlex`

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.11 installed
3. (Optional) Install `readline` for command history support:
   ```bash
   pip install readline
   ```

## Usage

### Running the Shell
```bash
python main.py
```

### Example Commands
```bash
[folder] mysh> pwd
/home/user/projects

[folder] mysh> cd ~/Documents
[Documents] mysh> ls
file1.txt  file2.txt  folder1

[Documents] mysh> echo "Hello $USER"
Hello username

[Documents] mysh> export MY_VAR=test_value
[Documents] mysh> echo $MY_VAR
test_value

[Documents] mysh> ls > output.txt
[Documents] mysh> cat output.txt
file1.txt  file2.txt  folder1  output.txt
```

## Testing

The project includes a comprehensive test suite to verify the security features:

```bash
python test_shell.py
```

The test suite validates:
- Environment variable name sanitization
- Path sanitization and validation
- Command name sanitization
- File redirection path validation
- Variable expansion with security checks
- Handling of potentially dangerous inputs

## Security Considerations

This shell implementation prioritizes security through:

1. **Input Sanitization**: All user input is sanitized before processing
2. **Path Validation**: File paths are validated to prevent access to unauthorized locations
3. **Command Restrictions**: Only alphanumeric characters, underscores, hyphens, and dots allowed in command names
4. **Environment Protection**: Environment variable names are sanitized to prevent injection
5. **Safe Redirection**: File redirection is restricted to safe locations

### Protected Against
- Command injection attacks
- Directory traversal attacks
- Environment variable injection
- Unsafe file operations
- Path traversal attempts
- System file modification

## File Structure
```
├── main.py           # Main shell implementation
├── test_shell.py     # Security test suite
└── README.md         # This file
```

## Requirements
- Python 3.11
- `readline` (optional, for command history)
- Cross-platform compatibility (Windows, Linux, macOS)

## Configuration

### History File
Command history is automatically saved to `~/.mysh_history` when readline is available.

### Environment Variables
The shell respects all standard environment variables and allows setting custom ones with the `export` command.

## Development

### Adding New Built-in Commands
To add a new built-in command:

1. Create a function following the pattern `builtin_commandname(args)`
2. Add security validation for any file operations or user input
3. Add the command check in the main loop
4. Update tests in `test_shell.py`

### Security Guidelines
- Always sanitize user input
- Validate file paths before operations
- Use the provided sanitization functions
- Test with the security test suite

## License

This project is provided as-is for educational and development purposes.

## Contributing

When contributing:
1. Maintain the security-first approach
2. Add tests for new features
3. Follow the existing code style
4. Document security considerations

## Known Limitations

- Limited pipe support (simple `>` and `>>` redirection only)
- No job control or background processes
- Simplified command parsing compared to full shells
- Some advanced shell features are not implemented for security reasons

---

**Note**: This shell prioritizes security over feature completeness. Some advanced shell features are intentionally omitted to maintain a secure execution environment.
