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
            self.view.show_yadisk_listdir(*self.model.get_yadisk_listdir())
            self.view.show_local_listdir(*self.model.get_local_listdir())


