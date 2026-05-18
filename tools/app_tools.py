import subprocess

class AppTools:

    @staticmethod
    def open_app(app_name):

        app_map = {
            "chrome": "start chrome",
            "vscode": "code",
            "notepad": "notepad",
            "calculator": "calc",
            "explorer": "explorer",
            "alilang": "explorer"
        }

        if not app_name:
            return "No app name provided."

        command = app_map.get(app_name.lower())

        if command:
            subprocess.Popen(command, shell=True)
            return f"Opened {app_name}"

        return f"Unknown app: {app_name}"