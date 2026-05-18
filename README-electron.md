# Electron Desktop App for Computer Agent

## Setup

1. Open a terminal in Project
2. Run `npm install`
3. Run `npm start`

## Notes

- The app launches an Electron window with a command input.
- Commands are sent to `python_bridge.py`.
- `python_bridge.py` uses your existing Python agent modules.
- If you need a specific Python executable, set the `PYTHON` environment variable before starting Electron.

Example:

```powershell
$env:PYTHON = 'python'
npm start
```
