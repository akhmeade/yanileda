# This Python file uses the following encoding: utf-8
from pathlib import Path
import os

class LocalModel:
    def get_listdir(self, path = None):
        if path is None:
            path = Path.cwd().as_posix()
        if not Path(path).is_dir():
            return None

        names = os.listdir(path)
        names.sort(key=lambda  x: Path(x).is_dir(), reverse=True)
        names = list(map(lambda x: (x,), names))
        return names, path