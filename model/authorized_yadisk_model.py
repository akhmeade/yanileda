# encoding: utf-8

import yadisk
from yadisk.exceptions import YaDiskError

from .imodel import IModel

import magic_const
import utils
from utils import Result

import logging
logger = logging.getLogger(__name__)

class AuthorizedYadiskModel(IModel):
    header = ("Type", "Name", "Last modified", "Size")

    def __init__(self):
        super().__init__()
        self.disk = yadisk.YaDisk(magic_const.APP_ID, magic_const.APP_SECRET)

    def get_verification_url(self):
        url = self.disk.get_code_url()
        return url
    
    @utils.yadisk_error_handle
    def set_verification_code(self, code):
        logger.info("Checking ver.code %s" % code)
        try:
            response = self.disk.get_token(code)
        except yadisk.exceptions.BadRequestError:
            return Result.failed("Wrong verification code")

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

        names = [self.header,]
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