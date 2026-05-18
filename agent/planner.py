import json
import re
import sys
from models.ollama_client import OllamaClient


SYSTEM_PROMPT = """
You are an AI desktop automation planner.

Convert user request into JSON actions.

AVAILABLE TOOLS:
1. open_app
2. google_search
3. youtube_search
4. read_file
5. find_file
6. find_folder
7. list_folder
8. get_path_info
9. open_path
10. write_text
11. press_key

Use find_file or find_folder when the user asks where a file or folder is located. Use read_file to read text from a known file path. Use list_folder to enumerate files inside a directory. Use open_app only for applications; use open_path for file system paths and URLs.

Output ONLY valid JSON.

Examples:
[
    {
        "tool": "open_app",
        "args": {
            "name": "chrome"
        }
    }
]

[
    {
        "tool": "open_path",
        "args": {
            "path": "https://www.google.com"
        }
    }
]

[
    {
        "tool": "find_file",
        "args": {
            "name": "example.txt",
            "root": "C:\\Users\\Nouman Masood"
        }
    }
]
"""


class Planner:

    def __init__(self):
        self.llm = OllamaClient()

    def _escape_backslashes(self, value):
        result = []
        i = 0

        while i < len(value):
            if value[i] == "\\":
                if i + 1 < len(value) and value[i + 1] in '"\\/bfnrtu':
                    result.append(value[i])
                    result.append(value[i + 1])
                    i += 2
                else:
                    result.append('\\\\')
                    i += 1
            else:
                result.append(value[i])
                i += 1

        return ''.join(result)

    def _sanitize_json_text(self, text):
        if not isinstance(text, str):
            return text

        start = text.find('[')
        if start == -1:
            return text

        end = text.rfind(']')
        json_text = text[start:end + 1] if end != -1 else text[start:].strip()
        if not json_text.endswith(']'):
            json_text += ']'

        def escape_match(match):
            inner = match.group(1)
            return f'"{self._escape_backslashes(inner)}"'

        return re.sub(r'"((?:[^"\\]|\\.)*)"', escape_match, json_text, flags=re.DOTALL)

    def create_plan(self, user_input):

        prompt = f"""
{SYSTEM_PROMPT}

USER REQUEST:
{user_input}
"""

        response = self.llm.generate(prompt)

        print("\nPlanner Response:\n", file=sys.stderr)
        print(response, file=sys.stderr)

        try:
            cleaned = self._sanitize_json_text(response)
            return json.loads(cleaned)

        except Exception as e:
            print("Planner parsing failed:", e, file=sys.stderr)
            return []