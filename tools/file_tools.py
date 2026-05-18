import os
from pathlib import Path
from string import ascii_uppercase


class FileTools:

    @staticmethod
    def get_drives():
        drives = []
        for letter in ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
        return drives

    @staticmethod
    def normalize_path(path):
        if path is None:
            return None
        return os.path.abspath(os.path.expanduser(path))

    @staticmethod
    def _walk_search(root, pattern, search_folders=False, max_results=20):
        results = []

        def on_error(error):
            return None

        for dirpath, dirnames, filenames in os.walk(root, topdown=True, onerror=on_error):
            candidates = dirnames if search_folders else filenames
            for entry in candidates:
                if pattern.lower() in entry.lower():
                    results.append(os.path.join(dirpath, entry))
                    if len(results) >= max_results:
                        return results
        return results

    @staticmethod
    def find_file(name, root=None, max_results=20):
        if not name:
            return "No file name provided."

        search_root = FileTools.normalize_path(root) if root else None
        search_roots = [search_root] if search_root else FileTools.get_drives()
        paths = []

        for root_path in search_roots:
            if not root_path or not os.path.exists(root_path):
                continue
            paths.extend(FileTools._walk_search(root_path, name, search_folders=False, max_results=max_results - len(paths)))
            if len(paths) >= max_results:
                break

        if not paths:
            return f"No files found matching '{name}'."

        return paths

    @staticmethod
    def find_folder(name, root=None, max_results=20):
        if not name:
            return "No folder name provided."

        search_root = FileTools.normalize_path(root) if root else None
        search_roots = [search_root] if search_root else FileTools.get_drives()
        paths = []

        for root_path in search_roots:
            if not root_path or not os.path.exists(root_path):
                continue
            paths.extend(FileTools._walk_search(root_path, name, search_folders=True, max_results=max_results - len(paths)))
            if len(paths) >= max_results:
                break

        if not paths:
            return f"No folders found matching '{name}'."

        return paths

    @staticmethod
    def list_folder(path='.'):  # pragma: no cover
        normalized = FileTools.normalize_path(path)
        if not os.path.exists(normalized):
            return f"Path does not exist: {normalized}"
        try:
            return [os.path.join(normalized, entry) for entry in os.listdir(normalized)]
        except PermissionError:
            return f"Permission denied: {normalized}"

    @staticmethod
    def get_path_info(path):
        if not path:
            return "No path provided."

        normalized = FileTools.normalize_path(path)
        if not os.path.exists(normalized):
            return f"Path not found: {normalized}"

        info = {
            "path": normalized,
            "is_file": os.path.isfile(normalized),
            "is_folder": os.path.isdir(normalized),
        }
        return info

    @staticmethod
    def read_file(path, max_bytes=200000):
        if not path:
            return "No path provided."

        normalized = FileTools.normalize_path(path)
        if not os.path.exists(normalized):
            return f"Path not found: {normalized}"

        if not os.path.isfile(normalized):
            return f"Path is not a file: {normalized}"

        try:
            with open(normalized, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(max_bytes)
        except Exception as e:
            return f"Failed to read file: {e}"

    @staticmethod
    def open_path(path):
        if not path:
            return "No path provided."

        normalized = FileTools.normalize_path(path)

        if os.path.exists(normalized):
            target = normalized
        else:
            target = path

        try:
            if os.name == 'nt':
                os.startfile(target)
            else:
                from subprocess import Popen
                from urllib.parse import urlparse
                parsed = urlparse(target)
                if parsed.scheme:
                    Popen(['xdg-open' if os.name == 'posix' else 'open', target])
                else:
                    Popen(['xdg-open' if os.name == 'posix' else 'open', normalized])
            return f"Opened: {target}"
        except Exception as e:
            return f"Failed to open path: {e}"
