# encoding: utf-8
import os

import yadisk

from .imodel import IModel

import magic_const

class YadiskModel(IModel):
    def __init__(self):
        super().__init__()

    def get_verification_url(self):
        self.disk = yadisk.YaDisk(magic_const.APP_ID, magic_const.APP_SECRET)
        self.url = self.disk.get_code_url()
        return self.url

    def set_verification_code(self, code):
        try:
            response = self.disk.get_token(code)
        except yadisk.exceptions.BadRequestError:
            return False

        self.disk.token = response.access_token

        #print("Check ver", self.disk.check_token())

        return self.disk.check_token()

    def get_listdir(self, path = None):
        if path is None:
            path = "disk:/"

        if not self.disk.is_dir(path):
            return None

        names = []
        for i in self.disk.listdir(path):
            names.append(
                (i.name, i.created.strftime(magic_const.DATETIME_FORMAT)))
        #print(names, path)
        
        return names, path
