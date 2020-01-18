# This Python file uses the following encoding: utf-8

import os

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal

from .file_systems import FileSystem

class MainWindow(QMainWindow):

    connect_to_yadisk_signal = pyqtSignal()
    get_yadisk_listdir = pyqtSignal(str)
    get_local_listdir = pyqtSignal(str)
    move_file_signal = pyqtSignal(str, str)

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
        self.local_files.double_clicked.connect(self.get_local_listdir)
        self.yadisk_files.double_clicked.connect(self.get_yadisk_listdir)
        self.yadisk_files.move_clicked.connect(self.move_file_from_yadisk)
        self.local_files.move_clicked.connect(self.move_file_from_local)

    def connect_to_yadisk(self):
        self.connect_to_yadisk_signal.emit()

    def show_status(self, message):
        self.statusBar().showMessage(message)

    def show_local_listdir(self, listdir, path):
        self.local_files.show_listdir(listdir, path)

    def show_yadisk_listdir(self, listdir, path):
        self.yadisk_files.show_listdir(listdir, path)
    def move_file_from_yadisk(self):
        from_path = self.yadisk_files.get_folder_path()
        to_path = self.local_files.get_folder_path()
        
        file_name = self.yadisk_files.get_file_name()
        from_path = os.path.join(from_path, file_name)
        to_path = os.path.join(to_path, file_name)
        self.move_file_signal.emit(from_path, to_path)

    def move_file_from_local(self):
        from_path = self.local_files.get_folder_path()
        to_path = self.yadisk_files.get_folder_path()
        
        file_name = self.local_files.get_file_name()
        from_path = os.path.join(from_path, file_name)
        to_path = os.path.join(to_path, file_name)
        self.move_file_signal.emit(from_path, to_path)



