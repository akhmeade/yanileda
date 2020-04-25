#encoding: utf-8

from urllib.parse import urlparse
from yadisk.exceptions import YaDiskError
from PyQt5.QtCore import QThread

import logging
logger = logging.getLogger(__name__)


def create_url(url, name=None):
    if name is None:
        name = url
    return '<a href="' + url + '">' + name + '</a>'


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def sizeof_fmt(num, suffix='b'):
    if num is None:
        return ""
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)


def yadisk_error_handle(fn):
    def wrapped(*args):
        try:
            result = fn(*args)
        except YaDiskError:
            logger.info("Connection problems")
            result = Result.failed("Connection problems to Yadisk")
        return result
    return wrapped


class Result:
    def __init__(self):
        self._is_ok = False
        self._result = None
        self._error_message = ""

    @staticmethod
    def success(result=True):
        obj = Result()
        obj._result = result
        obj._is_ok = True
        obj._error_message = ""
        return obj

    @staticmethod
    def failed(error_message):
        result = Result()
        result._is_ok = False
        result._error_message = error_message
        return result

    def result(self):
        return self._result

    def error_message(self):
        return self._error_message

    def is_ok(self):
        return self._is_ok


class Concurrent(QThread):
    def __init__(self, function, *args):
        super(Concurrent, self).__init__()
        self.func = function
        self.args = args
        self.result = Result.failed("Interrupt process")

    def run(self):
        logger.info("RUN CONCURRENT")
        self.result = self.func(*self.args)

    def get_result(self):
        return self.result
