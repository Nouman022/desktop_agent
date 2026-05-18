from pathlib import Path

path = Path(r'c:\Users\Nouman Masood\Desktop\Computer Agent\python_bridge.py')
text = path.read_text(encoding='utf-8')
old = '''    def extract_target(text):
        text = text.strip().rstrip(' ?.')
        text = re.sub(r'^(find|locate|search for|where is|where\'s|show me|show|list)\\b', '', text, flags=re.I).strip()
        text = re.sub(r'^(the|a|my|all)\\b', '', text, flags=re.I).strip()
        text = re.sub(r'^(file|folder|directory|dir|document|documents|files|folders|directories)\\b', '', text, flags=re.I).strip()
        text = re.sub(r'^(named|called)\\b', '', text, flags=re.I).strip()
        text = re.sub(r'^(in|inside|at)\\b', '', text, flags=re.I).strip()
        return text
'''
new = '''    def extract_target(text):
        text = text.strip().rstrip(' ?.')
        prefixes = [
            "find where is",
            "find where's",
            "where is",
            "where's",
            "find file named",
            "find folder named",
            "find directory named",
            "find file",
            "find folder",
            "find directory",
            "locate the file named",
            "locate the folder named",
            "locate the directory named",
            "locate file",
            "locate folder",
            "locate directory",
            "search for",
            "list files in",
            "list folders in",
            "list directories in",
            "show files in",
            "show folders in",
            "show directories in",
            "show",
            "list"
        ]
        for prefix in prefixes:
            if text.lower().startswith(prefix):
                text = text[len(prefix):].strip()
                break

        text = re.sub(r'^(the|a|my|all)\\s+', '', text, flags=re.I)
        text = re.sub(r'^(file|folder|directory|dir|document|documents|files|folders|directories)\\s+', '', text, flags=re.I)
        text = re.sub(r'^(named|called|in|inside|at)\\s+', '', text, flags=re.I)
        return text.strip().rstrip(' ?.')
'''
if old not in text:
    raise SystemExit('old pattern not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
print('patched')
