# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

from .connection_dialog import ConnectionDialog
from .file_systems import FileSystem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("forms/mainwindow.ui", self)
        self.local_file_system = FileSystem("Local file system")
        self.yandex_disk = FileSystem("Yandex Disk")
        self.layout.addWidget(self.local_file_system)
        self.layout.addWidget(self.yandex_disk)
        self.connect_to_actions()


    def connect_to_actions(self):
        self.connect_to_yadisk.triggered.connect(self.open_connection_dialog)

    def open_connection_dialog(self):
        self.dialog = ConnectionDialog("http:/habr.com")
        self.dialog.show()


