# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

from .file_systems import FileSystem

import utils

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/mainwindow.ui", self)
        self.layout.addWidget(FileSystem(utils.create_url("Local File System")))
        self.layout.addWidget(FileSystem("Yandex Disk"))


