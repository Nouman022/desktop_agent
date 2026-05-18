# Computer Agent

A desktop automation app built with Electron and Python. It allows the user to enter natural language commands in a desktop UI and routes them to a Python agent that can search files, open apps, read files, and inspect paths.

## Features

- Electron-based desktop interface
- Command input for dynamic system control
- Planner-driven Python automation pipeline
- File/folder search, open path, open app, and read file support

## Prerequisites

- Windows 10/11 or compatible desktop OS
- Node.js and npm
- Python 3.10+ installed and accessible

## Setup

1. Open the project folder in a terminal.
2. Install Electron dependencies:

```powershell
npm install
```

3. If needed, set the Python executable before running Electron:

```powershell
$env:PYTHON = 'python'
```

## Run

Start the Electron UI:

```powershell
npm start
```

Type a command in the desktop window, for example:

- `find where is resume`
- `open chrome`
- `list files in C:\Users\YourName\Desktop`

The app shows a planner output and the command result.

## Project Structure

- `electron-main.js` — Electron main process and window creation
- `preload.js` — Secure renderer API bridge
- `renderer.js` — UI logic and command handling
- `index.html` — Desktop UI layout and styles
- `python_bridge.py` — Electron-to-Python bridge for command execution
- `agent/` — Planner and executor modules
- `tools/` — System and file utilities
- `vision/` — OCR and screenshot utilities

## Notes

- The Electron app sends the command text to `python_bridge.py`.
- The Python bridge can fall back to direct search or use the planner to execute tools.
- Keep the entire project folder intact when sharing as a ZIP file to preserve dependencies and assets.

## Sharing

To share the project in a ZIP file, include the full workspace folder and keep the `package.json`, `electron-main.js`, `Python` files, and `agent/` and `tools/` folders.
