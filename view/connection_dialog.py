# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

import utils

class ConnectionDialog(QDialog):
    def __init__(self, url):
        super().__init__()
        uic.loadUi("forms/connection_dialog.ui", self)
        self.url_label.setText(utils.create_url(url))
        self.warning.hide()
    def accept(self):
        self.accepted.emit()

    def show_warning(self):
        self.warning.show()

