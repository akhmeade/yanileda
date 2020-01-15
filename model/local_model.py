# This Python file uses the following encoding: utf-8
import os

class LocalModel:
    def get_listdir(self, path = None):
        if path is None:
            path = os.getcwd()
        if not os.path.isdir(path):
            return None
        names = os.listdir(path)
        names = list(map(lambda x: (x,), names))
        return names, path