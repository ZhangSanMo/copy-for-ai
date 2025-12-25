# Code Context Extractor for AI

[![Build and Release](https://github.com/ZhangSanMo/copy-for-ai/actions/workflows/build-and-release.yml/badge.svg)](https://github.com/ZhangSanMo/copy-for-ai/actions/workflows/build-and-release.yml)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)](https://doc.qt.io/qtforpython/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

**Code Context Extractor** is a powerful, user-friendly GUI tool designed to help developers quickly select and copy code files from their projects to paste into AI assistants (like ChatGPT, Claude, Gemini, Copilot, etc.).

It solves the pain point of manually opening, copying, and pasting multiple files while ensuring binary files and irrelevant directories (like `.git`, `node_modules`) are automatically ignored.

![App Screenshot](doc/screenshot_placeholder.png)
*(Note: You can add a screenshot here)*

## ✨ Features

- **📂 Project Tree View**: Visualize your project structure and select specific files or entire folders.
- **🎨 Modern UI**: Built with PySide6, featuring a clean interface with **Dark/Light theme** support.
- **⚡ Smart Filtering**:
  - Automatically ignores common build artifacts and system directories (`.git`, `__pycache__`, `node_modules`, `dist`, etc.).
  - Skips binary files (images, executables, archives) to save context tokens.
- **clipboard Integration**: Merges selected files into a single Markdown-formatted text block and copies it directly to your clipboard.
- **🚀 One-File Executable**: Can be compiled into a single standalone `.exe` file for easy distribution.

## 🛠️ Installation & Running

### Option 1: Run from Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ZhangSanMo/copy-for-ai.git
   cd copy-for-ai
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python code_copier.py
   ```

### Option 2: Download Release

Go to the [Releases](https://github.com/ZhangSanMo/copy-for-ai/releases) page and download the latest `CodeContextExtractor.exe`. No Python installation is required.

## 📖 Usage

1. Launch the application.
2. Click **"Browse"** to select your project's root directory.
3. Use the file tree to check the files or folders you want to provide as context to the AI.
   - *Checked folders will recursively include all valid files inside them.*
4. Click **"Generate & Copy to Clipboard"**.
5. Paste the content directly into your AI chat interface.

## 🏗️ Building (Nuitka)

To compile the project into a standalone executable, we use [Nuitka](https://nuitka.net/).

**Build Command:**
```bash
python -m nuitka --standalone --onefile --enable-plugin=pyside6 --disable-console --disable-cache=all --output-filename=CodeContextExtractor.exe code_copier.py
```

## ⚙️ CI/CD (GitHub Actions)

This project includes a fully configured GitHub Actions workflow.
- **Trigger**: Pushing a tag starting with `v` (e.g., `v1.0.0`).
- **Action**: Automatically builds the `.exe` using Nuitka and publishes it to GitHub Releases.

To release a new version:
```bash
git tag v1.0.0
git push origin v1.0.0
```

## 📝 License

[MIT License](LICENSE) (or your preferred license)
