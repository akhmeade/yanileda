# encoding: utf-8

import yadisk

from .imodel import IModel

import magic_const

class AuthorizedYadiskModel(IModel):
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

        #print("Check ver", self.disk.check_token())

        return self.disk.check_token()

    def get_listdir(self, path=None):
        if path is None:
            path = magic_const.YADISK_PREFIX

        if not self.disk.is_dir(path):
            return None

        names = []
        listdir = list(self.disk.listdir(path))
        listdir.sort(key=lambda x: x.type == "dir", reverse=True)
        for i in listdir:
            names.append(
                (i.name, i.created.strftime(magic_const.DATETIME_FORMAT)))
        #print(names, path)
        
        return names, path
    
    def move_file(self, from_path, to_path):
        if from_path.startswith(magic_const.YADISK_PREFIX):
            self.download(from_path, to_path)
        else:
            self.upload(from_path, to_path)
    
    def upload(self, from_path, to_path):
        print('upload', from_path, to_path)
        self.disk.upload(from_path, to_path, overwrite=True)
    
    def download(self, from_path, to_path):
        print('download', from_path, to_path)
        self.disk.download(from_path, to_path)