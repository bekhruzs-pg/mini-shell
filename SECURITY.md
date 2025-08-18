# Security Policy

## Supported Versions

The following versions of MyShell are currently being supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Security Features

MyShell implements multiple layers of security to protect against common shell vulnerabilities:

### Input Sanitization
- **Command Validation**: Only alphanumeric characters, underscores, hyphens, and dots allowed in command names
- **Argument Sanitization**: All command arguments are validated and sanitized
- **Length Limits**: Commands are limited to 1000 characters to prevent buffer overflow attacks
- **Quote Handling**: Proper parsing of quoted strings using `shlex` library

### Path Security
- **Traversal Prevention**: Directory traversal attacks (e.g., `../../../etc/passwd`) are blocked
- **Path Canonicalization**: All paths are resolved and validated before use
- **System File Protection**: Access to critical system directories is restricted
- **Safe Navigation**: Directory changes are validated and restricted to safe locations

### Environment Protection
- **Variable Name Sanitization**: Environment variable names are restricted to safe characters
- **Value Validation**: Environment variable values are sanitized to prevent injection
- **System Variable Protection**: Critical system environment variables are protected

### File Operation Security
- **Redirection Validation**: Output redirection targets are validated for safety
- **System File Protection**: Cannot overwrite critical system files
- **Permission Checking**: File operations respect system permissions
- **Safe Modes**: File operations use safe defaults

### Command Execution Security
- **No Shell Injection**: Commands are executed without `shell=True` to prevent injection
- **Argument Isolation**: Each command argument is isolated and validated
- **Safe Defaults**: Secure execution is the default behavior

## Known Security Considerations

### By Design Limitations
- **Limited Pipe Support**: Advanced piping is intentionally limited for security
- **Restricted Command Set**: Some shell features are disabled to maintain security
- **No Background Jobs**: Job control features are omitted for security reasons
- **Simplified Parsing**: Complex shell syntax is not supported by design

### Platform-Specific Considerations
- **Windows**: Uses `cls` for clear command, validates Windows-specific paths
- **Unix/Linux**: Uses standard Unix commands with appropriate validation
- **Cross-platform**: Security measures adapt to the underlying operating system

## Reporting a Vulnerability

### How to Report
If you discover a security vulnerability in MyShell, please report it responsibly:

1. **DO NOT** create a public GitHub issue for security vulnerabilities  
2. Contact the maintainers privately through one of these methods:  
   - Email: [contact@fnbubbles420.org](mailto:contact@fnbubbles420.org)  
   - Create a private security advisory on GitHub  
   - Direct message to project maintainers  

### What to Include
When reporting a vulnerability, please include:
- **Description**: Clear description of the vulnerability
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Impact**: Assessment of the potential impact
- **Proof of Concept**: Safe demonstration of the vulnerability (if applicable)
- **Affected Versions**: Which versions are affected
- **Suggested Fix**: If you have suggestions for fixing the issue

### Response Timeline
- **Acknowledgment**: We will acknowledge receipt within 48 hours
- **Initial Assessment**: Initial security assessment within 7 days
- **Status Updates**: Regular updates every 7 days until resolution
- **Fix Timeline**: Security fixes will be prioritized and released as soon as possible

### Disclosure Policy
- We follow responsible disclosure practices
- Security fixes will be released before public disclosure
- Credit will be given to security researchers who report vulnerabilities responsibly
- Public disclosure will occur after fixes are available and users have had time to update

## Security Best Practices for Users

### Installation Security
- Download only from official sources
- Verify file checksums if provided
- Use virtual environments when possible
- Keep Python installation updated

### Usage Security
- **Principle of Least Privilege**: Run with minimal required permissions
- **Environment Isolation**: Use in isolated environments when possible
- **Regular Updates**: Keep the shell updated to the latest secure version
- **Audit Commands**: Review commands before execution in sensitive environments

### Configuration Security
- **History Files**: Secure history files with appropriate permissions
- **Environment Variables**: Be cautious with sensitive data in environment variables
- **File Permissions**: Ensure proper file permissions on shell scripts and configs

## Security Testing

### Automated Testing
The project includes comprehensive security tests:
```bash
python test_shell.py
