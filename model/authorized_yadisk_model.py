# encoding: utf-8

import yadisk

from .imodel import IModel

import magic_const

import logging
logger = logging.getLogger(__name__)

class AuthorizedYadiskModel(IModel):
    header = ("Type", "Name", "Last modified")

    def __init__(self):
        super().__init__()
        self.disk = yadisk.YaDisk(magic_const.APP_ID, magic_const.APP_SECRET)

    def get_verification_url(self):
        url = self.disk.get_code_url()
        return url

    def set_verification_code(self, code):
        try:
            response = self.disk.get_token(code)
        except yadisk.exceptions.BadRequestError:
            return False

        self.disk.token = response.access_token
         
        result = self.disk.check_token()
        if result:
            logger.info("Connected to Yadisk")
        else:
            logger.error("Cannot connect to Yadisk")
        
        return result

    def get_listdir(self, path=None):
        logger.info(path)
        if path is None:
            path = magic_const.YADISK_PREFIX

        if not self.disk.is_dir(path):
            return None

        names = [self.header,]
        listdir = list(self.disk.listdir(path))
        listdir.sort(key=lambda x: x.type == "dir", reverse=True)
        for i in listdir:
            names.append(
                (i.type, i.name, i.modified.strftime(magic_const.DATETIME_FORMAT)))
        
        return names, path
    
    def upload(self, from_path, to_path):
        logger.info("upload {} to {}".format(from_path, to_path))
        self.disk.upload(from_path, to_path, overwrite=True)
    
    def download(self, from_path, to_path):
        logger.info("download {} to {}".format(from_path, to_path))
        self.disk.download(from_path, to_path)