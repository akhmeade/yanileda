# This Python file uses the following encoding: utf-8

from pathlib import Path
import os
from datetime import datetime

import magic_const
import utils
import logging
logger = logging.getLogger(__name__)


def get_type(name):
    if name.is_dir():
        #print(name, "dir")
        return "dir"
    elif name.is_file():
        #print(name, "file")
        return "file"
    else:
        # print(name,"bad")
        return None


def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime(magic_const.DATETIME_FORMAT)
    return formated_date


class LocalModel:
    header = ("Type", "Name", "Last modified", "Size")

    def get_listdir(self, path=None):
        if path is None:
            path = Path.cwd().as_posix()
        if not Path(path).is_dir():
            return None

        names = os.listdir(path)
        path = Path(path)

        self.path = path
        names.sort(key=lambda x: (path / x).is_dir(), reverse=True)
        names = list(map(self.get_info, names))
        names.insert(0, self.header)

        return names, path.as_posix()

    def get_info(self, name):
        path = self.path
        file_type = get_type(path / name)
        mod_time = convert_date((path / name).stat().st_mtime)
        size = (path / name).stat().st_size
        size_str = utils.sizeof_fmt(size)
        return file_type, name, mod_time, size_str
