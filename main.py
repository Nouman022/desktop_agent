import re
from agent.planner import Planner
from agent.executor import Executor
from tools.file_tools import FileTools
from vision.screenshot import ScreenshotTool
from vision.ocr import OCRTool


planner = Planner()
executor = Executor()


def direct_file_search(command):
    normalized = command.strip()
    if not normalized:
        return False

    lower = normalized.lower()
    if not any(keyword in lower for keyword in ["find", "locate", "where is", "search for", "show me", "list", "display"]):
        return False

    if "open" in lower or "launch" in lower:
        return False

    if re.search(r'\b(list|show|display)\b', lower) and re.search(r'\b(folder|directory|files?|documents?)\b', lower):
        path_match = re.search(r'(?:in|inside|at|for)\s+(.+)', normalized, re.I)
        path = path_match.group(1).strip(" \"'") if path_match else normalized
        print(FileTools.list_folder(path))
        return True

    target = re.sub(r'^(find where is|find file named|find folder named|find file|find folder|find|locate the folder named|locate the file named|locate folder|locate file|locate|where is|search for|show me|show|list|display)\s*', '', normalized, flags=re.I)
    target = re.sub(r'\b(folder|directory|dir|file|named|called|the)\b', '', target, flags=re.I).strip(" \"'")

    if not target:
        return False

    if re.search(r'\b(folder|directory|dir)\b', lower):
        print(FileTools.find_folder(target))
    else:
        print(FileTools.find_file(target))
    return True


while True:

    print("\n========================")
    print("OLLAMA DESKTOP AGENT")
    print("========================")

    user_input = input("\nEnter command: ")

    if user_input.lower() == "exit":
        break

    if user_input.lower() == "screen":

        image_path = ScreenshotTool.capture()

        print(f"Screenshot saved: {image_path}")

        text = OCRTool.extract_text(image_path)

        print("\nOCR TEXT:\n")
        print(text)

        continue

    plan = planner.create_plan(user_input)

    print("\nGenerated Plan:\n")
    print(plan)

    executor.execute(plan)