# encoding: utf-8

from .imodel import IModel

class Model(IModel):
    def __init__(self):
        super().__init__()

    def get_verification_url(self):
        return "https://habr.com"
