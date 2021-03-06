# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication

from view.view import GuiView
from presenter.presenter import Presenter

from model.authorized_yadisk_model import AuthorizedYadiskModel
from model.bublic_yadisk_model import BublicYadiskModel
from model.local_model import LocalModel
from model.security_model import SecurityModel

import logging

import magic_const
logging.basicConfig(**magic_const.LOGGING_CONFIG)

if __name__ == "__main__":
    app = QApplication([])

    gui_view = GuiView()

    yadisk_model = AuthorizedYadiskModel()
    local_model = LocalModel()
    bublic_yadisk_model = BublicYadiskModel()
    security_model = SecurityModel()

    presenter = Presenter(gui_view, yadisk_model, local_model,
                          bublic_yadisk_model, security_model)

    gui_view.set_presenter(presenter)

    sys.exit(app.exec_())
