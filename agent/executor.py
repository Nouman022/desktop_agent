from tools.app_tools import AppTools
from tools.browser_tools import BrowserTools
from tools.file_tools import FileTools
from tools.keyboard_tools import KeyboardTools


class Executor:

    def execute(self, plan):

        for step in plan:

            tool = step.get("tool")
            args = step.get("args", {})

            print(f"Executing: {tool} -> {args}")

            if tool == "open_app":
                print(AppTools.open_app(args.get("app_name") or args.get("name")))

            elif tool == "google_search":
                print(BrowserTools.google_search(args.get("query")))

            elif tool == "youtube_search":
                print(BrowserTools.open_youtube(args.get("query")))

            elif tool == "find_file":
                print(FileTools.find_file(args.get("name"), args.get("root")))

            elif tool == "find_folder":
                print(FileTools.find_folder(args.get("name"), args.get("root")))

            elif tool == "list_folder":
                print(FileTools.list_folder(args.get("path")))

            elif tool == "get_path_info":
                print(FileTools.get_path_info(args.get("path")))

            elif tool == "open_path":
                print(FileTools.open_path(args.get("path")))

            elif tool == "read_file":
                print(FileTools.read_file(args.get("path")))

            elif tool == "write_text":
                KeyboardTools.write(args.get("text"))

            elif tool == "press_key":
                KeyboardTools.press(args.get("key"))