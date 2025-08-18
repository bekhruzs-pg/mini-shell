# Mini-Shell 🐚

A lightweight, cross-platform Python shell that mimics basic Unix/Windows commands with custom enhancements. Perfect for learning shell programming, command handling, and Python scripting.

---

## **Table of Contents**

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Commands](#commands)
* [Examples](#examples)
* [Contributing](#contributing)
* [License](#license)

---

## **Features**

* Cross-platform support (Windows & Unix-like systems)
* Built-in commands:

  * `ls` / `dir`
  * `pwd`
  * `cd`
  * `clear` / `cls`
  * `echo` (supports environment variables)
  * `export` (set environment variables)
  * `mkdir` / `rmdir`
  * Command output redirection (`>`)
* Handles errors gracefully for invalid paths or commands
* Command history with persistent storage (`~/.mysh_history`)
* Extensible structure for adding custom commands

---

## **Installation**

1. Clone the repository:

```bash
git clone https://github.com/bekhruzs-pg/mini-shell.git
cd mini-shell
```

2. (Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies (if any):

```bash
pip install -r requirements.txt
```

> No external dependencies required for basic usage.

---

## **Usage**

Run the shell using:

```bash
python main.py
```

You will see a prompt like:

```
[current_directory] mysh>
```

Type commands as you would in a regular terminal.

---

## **Supported Commands**

| Command            | Description                                            |
| ------------------ | ------------------------------------------------------ |
| `ls` / `dir`       | List files and directories                             |
| `pwd`              | Show current working directory                         |
| `cd <path>`        | Change directory                                       |
| `clear` / `cls`    | Clear the terminal                                     |
| `echo <text>`      | Print text or environment variables (`$HOME`, `$USER`) |
| `export KEY=VALUE` | Set environment variables                              |
| `mkdir <folder>`   | Create a new folder                                    |
| `rmdir <folder>`   | Remove an empty folder                                 |
| `<command> > file` | Redirect command output to a file                      |
| Any other command  | Executed via system shell                              |

---

## **Examples**

* Change directory:

```bash
[myproject] mysh> cd "Documents"
```

* List files:

```bash
[Documents] mysh> ls
```

* Print home directory:

```bash
[Documents] mysh> echo $HOME
```

* Create a folder:

```bash
[Documents] mysh> mkdir "New Folder"
```

* Export environment variable:

```bash
[Documents] mysh> export MY_VAR=123
```

* Redirect command output to a file:

```bash
[Documents] mysh> ls > output.txt
```

---

## **Contributing**

Contributions are welcome! Feel free to:

* Add new commands
* Improve cross-platform compatibility
* Fix bugs and improve error handling

Please fork the repository and submit pull requests.

---

## **License**

This project is licensed under the MIT License. See `LICENSE` for details.