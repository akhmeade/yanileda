#coding: utf-8

import yadisk
from yadisk.exceptions import TooManyRequestsError

import magic_const

class BublicYadiskModel:
    header = ("Type", "Name", "Public Url", "Last modified")
    def __init__(self):
        self.disk = yadisk.YaDisk()
    
    def check_url(self, url):
        print(url)
        result = None
        while result is None:

            try:
                is_correct = self.disk.public_exists(url)
                print(True)
                result = is_correct
            except TooManyRequestsError:
                print("too many")
                result = None
            except Exception as e:
                print(False)
                result = False
        return result
    
    def get_meta(self, url):
        print(url)
        info = self.disk.get_public_meta(url)
        return [self.header, 
            (info.type, info.name, info.public_url,
                info.created.strftime(magic_const.DATETIME_FORMAT))], url
    
    def get_listdir(self, url):
        if self.check_url(url):
            if self.disk.is_public_dir(url):
                listdir = list(self.disk.public_listdir(url))            
                listdir.sort(key=lambda x: x.type == "dir", reverse=True)
                
                names = [self.header,]
                for i in listdir:
                    names.append((i.type, i.name, i.public_url, i.modified.strftime(magic_const.DATETIME_FORMAT)))

                return names, url
        return None
        # if self.disk.is_public_dir(url):
        #     listdir = list(self.disk.public_listdir(url))
        #     listdir.sort(key=lambda x: x.type == "dir", reverse=True)
        #     names = []
        #     for i in listdir:
        #         names.append(
        #             (i.name, i.created.strftime(magic_const.DATETIME_FORMAT)))
        # else:
        #     file = self.disk.

    def download(self, from_path, to_path):
        if self.check_url(from_path):
            self.disk.download_public(from_path, to_path)
        