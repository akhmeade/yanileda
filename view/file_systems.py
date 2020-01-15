# This Python file uses the following encoding: utf-8

import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

class FileSystem(QWidget):
    double_clicked = pyqtSignal(str)

    def __init__(self, file_system_name):
        super().__init__()
        uic.loadUi("forms/file_system.ui", self)
        self.file_system_name.setText(file_system_name)
        self.listdir.doubleClicked.connect(self.double_click_slot)

    def show_listdir(self, listdir, path):

        self.path_box.setPlainText(path)

        if len(listdir) > 0:
            self.model = QStandardItemModel(len(listdir), len(listdir[0]))
        else:
            self.model = QStandardItemModel(len(listdir), 1)


        for n, file_info in enumerate(listdir):
            for m, info in enumerate(file_info):
                item = QStandardItem(info)
                self.model.setItem(n, m, item)
        self.listdir.setModel(self.model)
        self.listdir.resizeColumnsToContents()
    
    def double_click_slot(self, index):
        row = index.row()

        name = self.model.item(row).text()

        directory = self.path_box.toPlainText()
        path = os.path.join(directory, name)
        self.double_clicked.emit(path)

    
