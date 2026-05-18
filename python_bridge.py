import argparse
import json
import os
import re
import sys
import traceback

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from agent.planner import Planner
from tools.app_tools import AppTools
from tools.browser_tools import BrowserTools
from tools.file_tools import FileTools


def direct_search(command):
    lower = command.lower()
    if not any(keyword in lower for keyword in ["find", "locate", "where is", "search for", "list", "show"]):
        return None

    if any(keyword in lower for keyword in ["open ", "launch ", "start "]):
        return None

    def extract_target(text):
        text = text.strip().rstrip(' ?.')
        text = re.sub(r'^(find|locate|search for|show me|show|list)\b', '', text, flags=re.I).strip()
        text = re.sub(r'^(where is|where\'s)\b', '', text, flags=re.I).strip()
        text = re.sub(r'^(the|a|my|all)\b', '', text, flags=re.I).strip()
        text = re.sub(r'^(file|folder|directory|dir|document|documents|files|folders|directories)\b', '', text, flags=re.I).strip()
        text = re.sub(r'^(named|called)\b', '', text, flags=re.I).strip()
        text = re.sub(r'^(in|inside|at)\b', '', text, flags=re.I).strip()
        return text

    if re.search(r'\b(list|show|display)\b', lower) and re.search(r'\b(folder|directory|dir|files?|documents?)\b', lower):
        if ' in ' in lower:
            parts = re.split(r'\s+in\s+', command, flags=re.I, maxsplit=1)
            target = parts[1].strip() if len(parts) > 1 else extract_target(command)
        else:
            target = extract_target(command)
        if not target or target.lower() in ["list", "show", "display", "files", "folders", "documents", "directories"]:
            target = '.'
        results = FileTools.list_folder(target)
        return {"plan": [], "output": [str(results)]}

    target = extract_target(command)
    if not target:
        return None

    if re.search(r'\b(folder|directory|dir)\b', lower):
        results = FileTools.find_folder(target)
    else:
        results = FileTools.find_file(target)

    return {"plan": [], "output": [str(results)]}


class BridgeExecutor:
    def execute(self, plan):
        output = []

        for step in plan:
            tool = step.get("tool")
            args = step.get("args", {})
            output.append(f"Executing: {tool} -> {args}")

            if tool == "open_app":
                output.append(AppTools.open_app(args.get("app_name") or args.get("name")))

            elif tool == "google_search":
                output.append(BrowserTools.google_search(args.get("query")))

            elif tool == "youtube_search":
                output.append(BrowserTools.open_youtube(args.get("query")))

            elif tool == "find_file":
                output.append(str(FileTools.find_file(args.get("name"), args.get("root"))))

            elif tool == "find_folder":
                output.append(str(FileTools.find_folder(args.get("name"), args.get("root"))))

            elif tool == "list_folder":
                output.append(str(FileTools.list_folder(args.get("path"))))

            elif tool == "get_path_info":
                output.append(str(FileTools.get_path_info(args.get("path"))))

            elif tool == "open_path":
                output.append(str(FileTools.open_path(args.get("path"))))

            elif tool == "write_text":
                output.append("Typing text...")
                try:
                    from tools.keyboard_tools import KeyboardTools
                    KeyboardTools.write(args.get("text"))
                except Exception as err:
                    output.append(f"Keyboard action unavailable: {err}")

            elif tool == "press_key":
                output.append(f"Pressing key: {args.get('key')}")
                try:
                    from tools.keyboard_tools import KeyboardTools
                    KeyboardTools.press(args.get("key"))
                except Exception as err:
                    output.append(f"Keyboard action unavailable: {err}")

            else:
                output.append(f"Unknown tool: {tool}")

        return output


def main():
    parser = argparse.ArgumentParser(description="Python bridge for Electron Computer Agent")
    parser.add_argument("--command", required=True, help="The user command to execute")
    args = parser.parse_args()

    command = args.command.strip()
    fallback = direct_search(command)
    if fallback is not None:
        print(json.dumps(fallback, ensure_ascii=False))
        return

    planner = Planner()
    plan = planner.create_plan(command)
    executor = BridgeExecutor()
    output = executor.execute(plan)

    result = {
        "plan": plan,
        "output": output
    }

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        error = traceback.format_exc()
        print(json.dumps({"error": error}))
