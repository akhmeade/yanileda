# This Python file uses the following encoding: utf-8

class IView:
    """
    Interface of View in MVP-architecture
    """
    def set_presenter(self, presenter):
        raise NotImplementedError("Not implemented")

    def connect(self):
        raise NotImplementedError("Not implemented")

    def send_connection_code(self, code):
        raise NotImplementedError("Not implemented")



