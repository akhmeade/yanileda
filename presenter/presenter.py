# encoding: utf-8

from .ipresenter import IPresenter

import tempfile
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

class Presenter(IPresenter):
    def __init__(self, view, yadisk_model, local_model, bublic_yadisk_model,
        security_model):
        super().__init__()
        self.view = view
        
        self.yadisk_model = yadisk_model
        self.local_model = local_model
        self.bublic_yadisk_model = bublic_yadisk_model
        self.security_model = security_model

        self.get_local_listdir()

        self.temp_dir = tempfile.TemporaryDirectory()
        logger.info("temp.dir: %s" % self.temp_dir.name)

    def connect_to_yadisk(self):
        url = self.yadisk_model.get_verification_url()
        self.view.set_verification_url(url)

    def verificate_auth(self, code):
        is_verified = self.yadisk_model.set_verification_code(code)
        if not is_verified.is_ok():
            self.view.set_is_verified(False)
        else:
            self.view.set_is_verified(is_verified.result())
        
        if is_verified.result():
            self.get_yadisk_listdir()

    def get_yadisk_listdir(self, path=None):
        yadisk_listdir = self.yadisk_model.get_listdir(path)
        if yadisk_listdir.is_ok():
            self.view.show_yadisk_listdir(*yadisk_listdir.result())
        else:
            self.view.show_error(yadisk_listdir.error_message())
            
    
    def get_local_listdir(self, path=None):
        local_listdir = self.local_model.get_listdir(path)
        if not local_listdir is None:
            self.view.show_local_listdir(*local_listdir)

    def open_bublic_url(self, url):
        is_correct_url = self.bublic_yadisk_model.check_url(url)
        self.view.set_is_bublic_url_correct(is_correct_url)
        if is_correct_url:
            self.get_bublic_meta(url)
    
    def get_bublic_meta(self, url):
        listdir = self.bublic_yadisk_model.get_meta(url)

        if not listdir is None:
            self.view.show_yadisk_listdir(*listdir)
    
    def get_bublic_listdir(self, url):
        listdir = self.bublic_yadisk_model.get_listdir(url)

        if not listdir is None:
            self.view.show_yadisk_listdir(*listdir)

    def local_browse(self, key_type, algorithm):
        result = self.security_model.browse(key_type, algorithm)
        self.view.local_browse(result)
    
    def yadisk_browse(self, key_type, algorithm):
        result = self.security_model.browse(key_type, algorithm)
        self.view.yadisk_browse(result)

    def get_temp_path(self, filename):
        file_path = Path(filename)
        temp_dir_path = Path(self.temp_dir.name)
        return (temp_dir_path / file_path.name).as_posix()
    
    def download_from_auth_yadisk(self, from_path, to_path, encryption_data):
        temp_filename = self.get_temp_path(to_path)
        self.yadisk_model.download(from_path, temp_filename)
        self.security_model.decrypt(temp_filename, to_path, encryption_data)
    
    def download_from_bublic_yadisk(self, from_path, to_path, encryption_data):
        temp_filename = self.get_temp_path(to_path)
        self.bublic_yadisk_model.download(from_path, to_path)
        self.security_model.decypt(temp_filename, to_path, encryption_data)
    
    def upload_to_auth_yadisk(self, from_path, to_path, encryption_data):
        temp_filename = self.get_temp_path(from_path)
        self.security_model.encrypt(from_path, temp_filename, encryption_data)
        self.yadisk_model.upload(temp_filename, to_path)