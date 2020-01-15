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
        self.connect_to_actions()

    def connect_to_actions(self):
        self.listdir.doubleClicked.connect(self.double_click_slot)
        self.path_box.editingFinished.connect(self.get_listdir)
        self.back_button.clicked.connect(self.get_previous_folder)

    def show_listdir(self, listdir, path):

        self.path_box.setText(path)

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

        directory = self.path_box.text()
        path = os.path.join(directory, name)
        self.double_clicked.emit(path)

    def get_listdir(self):
        path = self.path_box.text()
        self.double_clicked.emit(path)
    
    def get_previous_folder(self):
        current = self.path_box.text()
        previous, _ = os.path.split(current)

        # if previous[-1] != '/' and previous[-1] != '\\':
        #     previous += "/"
        if previous == 'disk:':
            previous = 'disk:/'
        self.double_clicked.emit(previous)
