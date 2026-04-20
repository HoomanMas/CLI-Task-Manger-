# 📋 CLI Task Manager

> ⚡ A task manager built from scratch in two languages — C and Python — as a portfolio project demonstrating systems programming, file I/O, and GUI development.

![C](https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)

---

## 🚀 What is this?

A fully functional task manager with **two versions**:

| Version | Language | Interface | Storage |
|---------|----------|-----------|---------|
| 🖥️ Terminal | C | Command Line | Binary file |
| 🎨 Desktop | Python | GUI Window | JSON file |

> Same problem. Two languages. Two completely different approaches.

---

## ✨ Features

- ➕ Add tasks with title and priority
- ✅ Mark tasks as done
- 🗑️ Delete tasks
- 🔍 Filter by status (all / pending / done)
- 🎨 Color-coded priorities (high / medium / low)
- 💾 Data persists between sessions automatically

---

## 🖥️ C Version (Terminal)

### 🔨 Build

```bash
make
```

### ▶️ Usage

```bash
./task add "Buy groceries" high
./task add "Study for exam" medium
./task list
./task list pending
./task done 1
./task delete 2
./task list done
./task delete 1
```

### ⚙️ How it works

- Tasks are stored as raw C structs in a binary file `tasks.bin`
- `fwrite()` serializes the struct array to disk
- `fread()` loads it back on the next run
- Compiled with `gcc -Wall -Wextra -std=c11`

### 📁 File structure

```
cli-task-manager/
├── 📄 main.c        ← CLI commands and program entry point
├── 📄 storage.c     ← Binary file read and write
├── 📄 storage.h     ← Function declarations
├── 📄 task.h        ← Task struct and constants
└── 📄 Makefile      ← Build instructions
```

---

## 🎨 Python Version (GUI)

### ▶️ Run

```bash
python3 task_manager_gui.py
```

### ⚙️ How it works

- Built with Python's built-in `tkinter` library — zero external dependencies
- Tasks are stored in `tasks.json` using Python's `json` module
- Dark theme UI with color-coded priorities and status
- Click to select a task, then use buttons to act on it

### 📁 File structure

```
task-manager-gui/
├── 📄 task_manager_gui.py   ← Full GUI application
└── 📄 tasks.json            ← Auto-created when first task is added
```

---

## 🖼️ Preview

### Terminal version

```
ID    STATUS   PRIORITY  TITLE
────  ──────   ────────  ──────────────────────────
1     pending  high      Buy groceries
2     pending  medium    Study for exam
3     done     low       Call dentist
```

### GUI version

> Dark themed desktop window with input box, priority dropdown,
> color-coded task list, and Mark Done / Delete buttons.

---

## 🧠 What I learned

- 📌 C structs and binary file I/O with `fread` and `fwrite`
- 📌 `argc` and `argv` command-line argument parsing in C
- 📌 Header files and multi-file C project structure
- 📌 Makefiles and compiling with GCC
- 📌 Python OOP and building a GUI with tkinter
- 📌 JSON file handling in Python
- 📌 How the same problem looks completely different in two languages
- 📌 Using VS Code on Mac for C and Python development

---

## 🛠️ Requirements

### C version
- GCC compiler (`xcode-select --install` on Mac)
- Make

### Python version
- Python 3.x
- tkinter (built into Python — no install needed)

---

## ⚙️ Installation

### Clone the repo

```bash
git clone https://github.com/HoomanMas/cli-task-manager.git
cd cli-task-manager
```

### Run C version

```bash
make
./task add "My first task" high
./task list
```

### Run Python version

```bash
python3 task_manager_gui.py
```

---

## 📊 Project Stats

| Feature | C Version | Python Version |
|---------|-----------|----------------|
| Interface | Terminal CLI | Desktop GUI |
| Storage | Binary `.bin` file | JSON file |
| Dependencies | None | None |
| Lines of code | ~200 | ~180 |
| Build required | Yes (make) | No |

---

## 👨‍💻 Author

**Hooman Mas** — Seneca College, Computer Programming

🎓 Built as a resume project to demonstrate cross-language development skills across C and Python.

🔗 [GitHub Profile](https://github.com/HoomanMas)

---

⭐ *If you found this useful, give it a star!* ⭐
