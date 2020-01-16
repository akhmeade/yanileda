# This Python file uses the following encoding: utf-8

class IView:
    """
    Interface of View in MVP-architecture
    """
    def set_presenter(self, presenter):
        raise NotImplementedError("Not implemented")

    def connect_to_yadisk(self):
        raise NotImplementedError("Not implemented")

    def set_verification_url(self, url):
        raise NotImplementedError("Not implemented")

    def send_verification_code(self):
        raise NotImplementedError("Not implemented")