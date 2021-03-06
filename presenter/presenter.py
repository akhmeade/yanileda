# encoding: utf-8

import tempfile
from pathlib import Path

from magic_const import KeyType
from utils import Result
from utils import Concurrent

import logging
logger = logging.getLogger(__name__)


class Presenter:

    def __init__(self, view, yadisk_model, local_model, bublic_yadisk_model,
                 security_model):
        super().__init__()
        self.view = view

        self.yadisk_model = yadisk_model
        self.local_model = local_model
        self.bublic_yadisk_model = bublic_yadisk_model
        self.security_model = security_model

        self.temp_dir = tempfile.TemporaryDirectory()
        logger.info("temp.dir: %s" % self.temp_dir.name)
        self.get_local_listdir()

    def check_result(self, result):
        if result.is_ok():
            return True
        else:
            self.view.show_error(result.error_message())
            return False

    def connect_to_yadisk(self):
        url = self.yadisk_model.get_verification_url()
        self.view.set_verification_url(url)

    def run_time_consuming(self, message, func, *args):
        concurrent = Concurrent(func, *args)
        concurrent.finished.connect(self.view.close_progress_dialog)
        concurrent.start()
        self.view.show_progress_dialog(message)
        return concurrent.get_result()

    def verificate_auth(self, code):
        is_verified = self.run_time_consuming("Code verification...",
                                              self.yadisk_model.set_verification_code, code)

        if not self.check_result(is_verified):
            return

        self.view.set_is_verified(is_verified.result())

        if is_verified.result():
            self.get_yadisk_listdir()

    def get_yadisk_listdir(self, path=None):
        yadisk_listdir = self.yadisk_model.get_listdir(path)
        if not self.check_result(yadisk_listdir):
            return
        self.view.show_yadisk_listdir(*yadisk_listdir.result())

    def get_local_listdir(self, path=None):
        local_listdir = self.local_model.get_listdir(path)
        if not local_listdir is None:
            self.view.show_local_listdir(*local_listdir)

    def open_bublic_url(self, url):
        is_correct_url = self.bublic_yadisk_model.check_url(url)
        if not self.check_result(is_correct_url):
            return

        self.view.set_is_bublic_url_correct(is_correct_url.result())

        if is_correct_url.result():
            self.get_bublic_meta(url)

    def get_bublic_meta(self, url):
        listdir = self.bublic_yadisk_model.get_meta(url)

        if not self.check_result(listdir):
            return

        self.view.show_yadisk_listdir(*listdir.result())

    def get_bublic_listdir(self, url):
        listdir = self.bublic_yadisk_model.get_listdir(url)

        if not self.check_result(listdir):
            return

        self.view.show_yadisk_listdir(*listdir.result())

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

    def check_media(self, crypto_data):
        key_type = crypto_data["key_type"]
        media_path = crypto_data["media_path"]
        take_file_from_yadisk = crypto_data["take_file_from_yadisk"]
        if key_type in (KeyType.new_media, KeyType.existing_media):
            if take_file_from_yadisk:
                result = self.yadisk_model.download_media(
                    media_path, self.temp_dir.name)
                #result = self.yadisk_model.download_media(media_path, "D:/yanileda/trash")
                return result

            else:
                return Result.success(media_path)
        else:
            return Result.success(media_path)

    def download_from_auth_yadisk(self, from_path, to_path, crypto_data):
        media_path = self.check_media(crypto_data)
        logger.info("download from yadisk %s %s %s" %
                    (from_path, to_path, crypto_data))
        if not self.check_result(media_path):
            return
        crypto_data["media_path"] = media_path.result()
        logger.info("download from yadisk %s" % crypto_data)

        temp_filename = self.get_temp_path(to_path)
        download_result = self.yadisk_model.download(from_path, temp_filename)

        if not self.check_result(download_result):
            return

        decrypt_result = self.security_model.decrypt(
            temp_filename, to_path, crypto_data)
        if not self.check_result(decrypt_result):
            return

    def download_from_bublic_yadisk(self, from_path, to_path, crypto_data):
        media_path = self.check_media(crypto_data)
        if not self.check_result(media_path):
            return
        crypto_data["media_path"] = media_path.result()

        temp_filename = self.get_temp_path(to_path)
        download_result = self.bublic_yadisk_model.download(from_path, to_path)
        if not self.check_result(download_result):
            return

        decrypt_result = self.security_model.decypt(
            temp_filename, to_path, crypto_data)
        if not self.check_result(decrypt_result):
            return

    def upload_to_auth_yadisk(self, from_path, to_path, crypto_data):
        logger.info("Upload to yadisk_1 %s" % crypto_data)
        media_path = self.check_media(crypto_data)
        if not self.check_result(media_path):
            return
        crypto_data["media_path"] = media_path.result()
        logger.info("Upload to yadisk_2 %s" % crypto_data)

        temp_filename = self.get_temp_path(from_path)
        encrypt_result = self.run_time_consuming("Encrypting...",
                                                 self.security_model.encrypt,
                                                 from_path, temp_filename, crypto_data)

        if not self.check_result(encrypt_result):
            return

        upload_result = self.run_time_consuming("Uploading to YaDisk...",
                                                self.yadisk_model.upload,
                                                temp_filename, to_path)
        #upload_result = self.yadisk_model.upload(temp_filename, to_path)
        if not self.check_result(upload_result):
            return

    def get_key(self, algorithm, key_type):
        return self.security_model.get_key_for_presenter(algorithm, key_type)

    def get_local_key(self, algorithm, key_type):
        key = self.get_key(algorithm, key_type)
        logger.info("Key %s" % key)
        self.view.put_local_key(key)

    def get_yadisk_key(self, algorithm, key_type):
        key = self.get_key(algorithm, key_type)
        self.view.put_yadisk_key(key)

    def set_media_folder(self, path):
        result = self.yadisk_model.set_media_folder(path)
        self.check_result(result)
