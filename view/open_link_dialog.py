from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

import utils

class OpenLinkDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("forms/open_link_dialog.ui", self)
        self.warning_label.hide()
    def accept(self):
        self.accepted.emit()
    
    def get_bublic_url(self):
        return self.url_box.text()

    def show_warning(self):
        self.warning_label.show()
    
    def get_tab_name(self):
        return self.name_box.text()