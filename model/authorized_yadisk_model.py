# encoding: utf-8

import yadisk
import time
import magic_const
import utils
from utils import Result
from pathlib import Path

import logging
logger = logging.getLogger(__name__)


class AuthorizedYadiskModel:
    header = ("Type", "Name", "Last modified", "Size")

    def __init__(self):
        super().__init__()
        self.disk = yadisk.YaDisk(magic_const.APP_ID, magic_const.APP_SECRET)
        self.media_folder = ""

    def get_verification_url(self):
        url = self.disk.get_code_url()
        return url

    @utils.yadisk_error_handle
    def set_verification_code(self, code):
        logger.info("Checking ver.code %s" % code)
        # time.sleep(5)

        try:
            response = self.disk.get_token(code)
        except yadisk.exceptions.BadRequestError:
            return Result.success(False)

        self.disk.token = response.access_token

        result = self.disk.check_token()
        if result:
            logger.info("Connected to Yadisk")
        else:
            logger.error("Cannot connect to Yadisk")

        return Result.success(result)

    @utils.yadisk_error_handle
    def get_listdir(self, path=None):
        logger.info("Open path %s" % path)
        if path is None:
            path = magic_const.YADISK_PREFIX

        if not self.disk.is_dir(path):
            return Result.failed("Path doesn't exist")

        names = [self.header, ]
        listdir = list(self.disk.listdir(path))
        listdir.sort(key=lambda x: x.type == "dir", reverse=True)
        for i in listdir:
            names.append(self.get_info(i))

        return Result.success((names, path))

    def get_info(self, file):
        file_type = file.type
        name = file.name
        mod_tyme = file.modified.strftime(magic_const.DATETIME_FORMAT)
        size = utils.sizeof_fmt(file.size)
        return file_type, name, mod_tyme, size

    @utils.yadisk_error_handle
    def upload(self, from_path, to_path):
        logger.info("upload {} to {}".format(from_path, to_path))

        self.disk.upload(from_path, to_path, overwrite=True)
        return Result.success(True)

    @utils.yadisk_error_handle
    def download(self, from_path, to_path):
        logger.info("download {} to {}".format(from_path, to_path))
        self.disk.download(from_path, to_path)
        return Result.success(True)

    @utils.yadisk_error_handle
    def set_media_folder(self, path):
        logger.info("set media folder %s" % path)
        if not self.disk.exists(path):
            return Result.failed("Media path '%s' doesn't exists" % path)

        if not self.disk.is_dir(path):
            Result.failed("Media path '%s' isn't directory" % path)

        self.media_folder = path
        return Result.success(True)

    @utils.yadisk_error_handle
    def download_media(self, media_name, dir_name):
        # check media
        media_path = Path(self.media_folder) / media_name
        logger.info("Check path %s" % media_path.as_posix())

        if not self.disk.exists(media_path.as_posix()):
            return Result.failed("Media path isn't found")

        temp_path = Path(dir_name) / media_name

        download_result = self.download(
            media_path.as_posix(), temp_path.as_posix())

        if download_result.is_ok():
            if download_result.result():
                return Result.success(temp_path.as_posix())
            else:
                return Result.failed("Something has gone wrong")
        else:
            return download_result
