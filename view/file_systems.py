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

        if len(listdir) > 0:
            model = QStandardItemModel(len(listdir), len(listdir[0]))
        else:
            model = QStandardItemModel(len(listdir), 1)


        for n, file_info in enumerate(listdir):
            for m, info in enumerate(file_info):
                item = QStandardItem(info)
                model.setItem(n, m, item)
        self.listdir.setModel(model)
        self.listdir.resizeColumnsToContents()
