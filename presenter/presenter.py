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
        if not self.model.set_verification_code(code):
            print("BAD")

