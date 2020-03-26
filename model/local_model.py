# This Python file uses the following encoding: utf-8
from pathlib import Path
import os
from datetime import datetime

import magic_const

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

def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime(magic_const.DATETIME_FORMAT)
    return formated_date

class LocalModel:
    header = ("Type", "Name", "Last modified")

    
    def get_listdir(self, path = None):
        if path is None:
            path = Path.cwd().as_posix()
        if not Path(path).is_dir():
            return None

        names = os.listdir(path)
        path = Path(path)
        
        names.sort(key=lambda  x: (path / x).is_dir(), reverse=True)
        names = list(map(lambda x: (get_type(path / x), x, convert_date((path / x).stat().st_mtime)), names))
        names.insert(0, self.header)
        

        return names, path.as_posix()