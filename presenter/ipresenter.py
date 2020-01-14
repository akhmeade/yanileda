# encoding: utf-8

class IPresenter:
    def connect_to_yadisk(self):
        raise NotImplementedError("Not implemented")

    def verificate_auth(self, code):
        raise NotImplementedError("Not implemented")
