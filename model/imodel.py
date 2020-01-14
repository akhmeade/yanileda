# encoding: utf-8

class IModel:
    def get_verification_url(self):
        raise NotImplementedError("Not implemented")

    def set_verification_code(self, code):
        raise NotImplementedError("Not implemented")

    def get_yadisk_listdir(self, path = 'disk:/'):
        raise NotImplementedError("Not implemented")

