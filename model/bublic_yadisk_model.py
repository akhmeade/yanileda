#coding: utf-8

import yadisk
from yadisk.exceptions import TooManyRequestsError
from yadisk.exceptions import NotFoundError

import magic_const
import utils

from utils import Result

import logging
logger = logging.getLogger(__name__)


def avoid_too_many_requests_error(fn):
    def wrapped(*args):
        result = None
        while result is None:
            try:
                result = fn(*args)
            except TooManyRequestsError:
                logger.info("Too many requests")
                result = None
        return result
    return wrapped


class BublicYadiskModel:
    header = ("Type", "Name", "Public Url", "Last modified", "Size")

    def __init__(self):
        self.disk = yadisk.YaDisk()

    @avoid_too_many_requests_error
    @utils.yadisk_error_handle
    def check_url(self, url):
        logger.info("check url " + url)
        try:
            result = self.disk.public_exists(url)
        except NotFoundError:
            result = False
        return Result.success(result)

    @avoid_too_many_requests_error
    @utils.yadisk_error_handle
    def get_meta(self, url):
        logger.info("get meta " + url)
        info = self.disk.get_public_meta(url)
        return Result.success(([self.header,
                                (info.type, info.name, info.public_url,
                                 info.created.strftime(magic_const.DATETIME_FORMAT))], url))

    @avoid_too_many_requests_error
    @utils.yadisk_error_handle
    def get_listdir(self, url):
        if self.check_url(url):
            if self.disk.is_public_dir(url):
                listdir = list(self.disk.public_listdir(url))
                listdir.sort(key=lambda x: x.type == "dir", reverse=True)

                names = [self.header, ]
                for i in listdir:
                    names.append(self.get_info(i))

                return Result.success((names, url))
            else:
                return Result.failed("Url isn't public")
        return Result.failed("Url doesnt't exist")
        # if self.disk.is_public_dir(url):
        #     listdir = list(self.disk.public_listdir(url))
        #     listdir.sort(key=lambda x: x.type == "dir", reverse=True)
        #     names = []
        #     for i in listdir:
        #         names.append(
        #             (i.name, i.created.strftime(magic_const.DATETIME_FORMAT)))
        # else:
        #     file = self.disk.

    def get_info(self, file):
        file_type = file.type
        name = file.name
        public_url = file.public_url
        mod_tyme = file.modified.strftime(magic_const.DATETIME_FORMAT)
        size = utils.sizeof_fmt(file.size)

        return file_type, name, public_url, mod_tyme, size

    @avoid_too_many_requests_error
    @utils.yadisk_error_handle
    def download(self, from_path, to_path):
        if self.check_url(from_path):
            self.disk.download_public(from_path, to_path)
            return Result.success(True)
