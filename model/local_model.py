# This Python file uses the following encoding: utf-8
from pathlib import Path
import os

def get_type(name):
    if name.is_dir():
        #print(name, "dir")
        return "dir"
    elif name.is_file():
        #print(name, "file")
        return "file"
    else:
        #print(name,"bad")
        return None

class LocalModel:
    def get_listdir(self, path = None):
        if path is None:
            path = Path.cwd().as_posix()
        if not Path(path).is_dir():
            return None

        names = os.listdir(path)
        path = Path(path)
        names.sort(key=lambda  x: (path / x).is_dir(), reverse=True)
        names = list(map(lambda x: (get_type(path / x), x), names))


        return names, path.as_posix()