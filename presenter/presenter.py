# encoding: utf-8

from .ipresenter import IPresenter

class Presenter(IPresenter):
    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model

    def connect_to_yadisk(self):
        url = self.model.get_verification_url()
        self.view.set_verification_url(url)

    def verificate_auth(self, code):
        is_verified = self.model.set_verification_code(code)
        self.view.set_is_verified(is_verified)
        if is_verified:
            self.get_yadisk_listdir()
            self.get_local_listdir()

    def get_yadisk_listdir(self, path = None):
        print(path)
        yadisk_listdir = self.model.get_yadisk_listdir(path)
        if not yadisk_listdir is None:
            self.view.show_yadisk_listdir(*yadisk_listdir)
    
    def get_local_listdir(self, path = None):
        local_listdir = self.model.get_local_listdir(path)
        if not local_listdir is None:
            self.view.show_local_listdir(*local_listdir)


