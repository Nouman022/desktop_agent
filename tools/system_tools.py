import os


class SystemTools:

    @staticmethod
    def list_files(path="."):
        return os.listdir(path)