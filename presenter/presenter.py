# encoding: utf-8

from .ipresenter import IPresenter

class Presenter(IPresenter):
    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
