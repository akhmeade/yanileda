# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

class FileSystem(QWidget):
    def __init__(self, file_system_name):
        super().__init__()
        uic.loadUi("view/file_system.ui", self)
        self.file_system_name.setText(file_system_name)
