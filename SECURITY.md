---

# Security Policy

## Overview

This project provides a restricted shell environment for users. Its primary security goal is to **prevent directory traversal, arbitrary command execution, and unauthorized system access**. All user actions are sandboxed to operate only within their designated directory.

---

## Threat Model

The following attack vectors are explicitly considered:

* **Path Traversal** (`../`, symlinks, `..\\`)
* **Command Injection** (e.g., `; rm -rf /`)
* **Arbitrary Binary Execution** (running programs outside the allowlist)
* **Sandbox Escape** (accessing `/etc`, `$HOME/.ssh`, etc.)

---

## Security Mechanisms

1. **Path Restrictions**

   * All paths are normalized with `os.path.realpath`.
   * Access is denied if paths resolve outside the user’s sandbox directory.

2. **Filename Validation**

   * Filenames must match the regex:

     ```regex
     ^[a-zA-Z0-9_.\-]+$
     ```
   * Prevents injection of metacharacters (`;`, `|`, `&`, spaces).

3. **Safe Directory**

   * A dedicated `outputs/` directory is created as the default working directory.
   * Users cannot escape this directory.

4. **Allowed Commands Only**

   * Only predefined commands are executable (e.g., `ls`, `pwd`, `cat`).
   * All execution is done with `shell=False`.
   * Any request outside the allowlist is rejected.

5. **Delegation to Built-ins**

   * Common commands like `pwd` or `echo` may be implemented directly in Python instead of relying on external binaries.

---

## Allowed Commands

The following commands are permitted:

* Navigation: `ls`, `pwd`, `stat`
* File viewing: `cat`, `head`, `tail`
* Output: `echo`
---

## Reporting a Vulnerability

If you discover a security vulnerability in this project:

1. Do not publicly disclose the issue.
2. Contact the maintainer directly via email.
3. Provide detailed steps to reproduce the vulnerability.

---

⚠️ **Important**: This restricted shell is **not a replacement for OS-level sandboxing** (e.g., Docker, chroot, namespaces). It should always be run in an isolated environment.
