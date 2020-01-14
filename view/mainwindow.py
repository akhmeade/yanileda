# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal

from .file_systems import FileSystem

class MainWindow(QMainWindow):

    connect_to_yadisk_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi("forms/mainwindow.ui", self)
        self.local_files = FileSystem("Local file system")
        self.yadisk_files = FileSystem("Yandex Disk")
        self.layout.addWidget(self.local_files)
        self.layout.addWidget(self.yadisk_files)
        self.connect_to_actions()
        self.show_status("Not connected")


    def connect_to_actions(self):
        self.connect_to_yadisk_action.triggered.connect(self.connect_to_yadisk)

    def connect_to_yadisk(self):
        self.connect_to_yadisk_signal.emit()

    def show_status(self, message):
        self.statusBar().showMessage(message)

    def show_local_listdir(self, listdir, path):
        self.local_files.show_listdir(listdir, path)

    def show_yadisk_listdir(self, listdir, path):
        self.yadisk_files.show_listdir(listdir, path)


