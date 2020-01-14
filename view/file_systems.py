# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem

from PyQt5 import uic

class FileSystem(QWidget):
    def __init__(self, file_system_name):
        super().__init__()
        uic.loadUi("forms/file_system.ui", self)
        self.file_system_name.setText(file_system_name)

    def show_listdir(self, listdir, path):

        self.path_box.setPlainText(path)

        model = QStandardItemModel(len(listdir), 1)

        for n, name in enumerate(listdir):
            item = QStandardItem(name)
            model.setItem(n, 0, item)
        self.listdir.setModel(model)
