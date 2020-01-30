# This Python file uses the following encoding: utf-8

from pathlib import Path

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

import magic_const

class FileSystem(QWidget):
    double_clicked = pyqtSignal(str)
    move_clicked = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        uic.loadUi("forms/file_system.ui", self)
        #self.file_system_name.setText(file_system_name)
        self.connect_to_actions()
        self.model = None

    def connect_to_actions(self):
        self.listdir.doubleClicked.connect(self.double_click_slot)
        self.path_box.editingFinished.connect(self.get_listdir)
        self.back_button.clicked.connect(self.get_previous_folder)
        self.load_button.clicked.connect(self.move_clicked)

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

        directory = Path(self.path_box.text())
        path = directory / name
        self.double_clicked.emit(path.as_posix())

    def get_listdir(self):
        path = self.path_box.text()
        self.double_clicked.emit(path)
    
    def get_previous_folder(self):
        current = Path(self.path_box.text())
        previous = current.parent.as_posix()
        # if previous[-1] != '/' and previous[-1] != '\\':
        #     previous += "/"
        if previous == 'disk:':
            previous = magic_const.YADISK_PREFIX
        self.double_clicked.emit(previous)
    
    def get_folder_path(self):
        return self.path_box.text()

    def get_file_name(self):
        selected = self.listdir.selectedIndexes()
        if len(selected) < 1:
            print("BAD SELECTED")
        selected = selected[0]
        row = selected.row()
        file_name = self.model.item(row).text()
        return file_name