# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal

from .connection_dialog import ConnectionDialog
from .file_systems import FileSystem

class MainWindow(QMainWindow):

    connect_to_yadisk_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi("forms/mainwindow.ui", self)
        self.local_file_system = FileSystem("Local file system")
        self.yandex_disk = FileSystem("Yandex Disk")
        self.layout.addWidget(self.local_file_system)
        self.layout.addWidget(self.yandex_disk)
        self.connect_to_actions()


    def connect_to_actions(self):
        self.connect_to_yadisk_action.triggered.connect(self.connect_to_yadisk)

    def connect_to_yadisk(self):
        self.connect_to_yadisk_signal.emit()


