# This Python file uses the following encoding: utf-8

from pathlib import Path

from PyQt5.QtWidgets import QWidget

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

import magic_const

import resources

class FileSystem(QWidget):
    double_clicked = pyqtSignal(str)
    move_clicked = pyqtSignal()

    def __init__(self, label_names, parent=None):
        QWidget.__init__(self, parent)
        uic.loadUi("forms/file_system.ui", self)
        #self.file_system_name.setText(file_system_name)
        self.connect_to_actions()
        self.model = None
        self.protocol = []

        self.folder_icon = QIcon(":/img/images/folder_icon.png")
        self.file_icon = QIcon(":/img/images/file_icon.png")

        self.set_label_names(label_names)

        self.fill_combobox(self.algorithms_box, magic_const.SecurityAlgorithm)
        self.fill_combobox(self.key_type_box, magic_const.KeyType)

    def connect_to_actions(self):
        self.listdir.doubleClicked.connect(self.double_click_slot)
        self.path_box.editingFinished.connect(self.get_listdir)
        self.back_button.clicked.connect(self.get_previous_folder)
        self.load_button.clicked.connect(self.move_clicked)
    
    def set_label_names(self, label_names):
        self.message_label.setText(label_names["message_label"])
        self.algorithm_label.setText(label_names["algorithm_label"])
        self.key_type_label.setText(label_names["key_type_label"])
        self.load_button.setText(label_names["load_button"])
    
    def fill_combobox(self, combobox, EnumClass):
        items = list(EnumClass)
        add_item = lambda item: combobox.addItem(item.value, item)
        list(map(add_item, items))

    def show_listdir(self, listdir, path):
        header = listdir[0]
        listdir = listdir[1:]
        self.protocol.append(path)
        self.path_box.setText(path)

        if len(listdir) > 0:
            self.model = QStandardItemModel(len(listdir), len(listdir[0]))
        else:
            self.model = QStandardItemModel(len(listdir), 1)

        self.model.setHorizontalHeaderLabels(header)
        item = QStandardItem("..")
        self.model.setItem(0, 1, item)
        item = QStandardItem(self.folder_icon, "")
        self.model.setItem(0, 0, item)
        for n, file_info in enumerate(listdir):
            if file_info[0] == "dir":
                item = QStandardItem(self.folder_icon, "")
            elif file_info[0] == "file":
                item = QStandardItem(self.file_icon, "")
            self.model.setItem(n+1, 0, item)
            for m, info in enumerate(file_info[1:], 1):
                item = QStandardItem(info)
                self.model.setItem(n + 1, m, item)
        self.listdir.setModel(self.model)
        self.listdir.resizeColumnsToContents()
    
    def double_click_slot(self, index):
        row = index.row()
        name = self.model.item(row, 1).text()

        directory = Path(self.path_box.text())
        if row == 0:
            path = directory.parent
        else:
            path = directory / name
        if path.as_posix() == "disk:":
            self.double_clicked.emit(magic_const.YADISK_PREFIX)
        else:
            self.double_clicked.emit(path.as_posix())

    def get_listdir(self):
        path = self.path_box.text()
        path = Path(path)
        self.double_clicked.emit(path.as_posix())
    
    def get_previous_folder(self):
        if len(self.protocol) < 2:
            return
        previous = self.protocol[-2]
        self.protocol = self.protocol[:-2]
        self.double_clicked.emit(previous)
        # current = Path(self.path_box.text())
        # previous = current.parent.as_posix()
        # # if previous[-1] != '/' and previous[-1] != '\\':
        # #     previous += "/"
        # if previous == 'disk:':
        #     previous = magic_const.YADISK_PREFIX
        # self.double_clicked.emit(previous)
    
    def get_folder_path(self):
        return self.path_box.text()

    def get_file_name(self):
        selected = self.listdir.selectedIndexes()
        if len(selected) < 1:
            print("BAD SELECTED")
        selected = selected[1]
        row = selected.row()
        file_name = self.model.item(row, 1).text()
        return file_name
    
    def get_algorithm(self):
        return self.algorithms_box.currentData()


class BublicFileSystem(FileSystem):
    def __init__(self, parent=None):
        FileSystem.__init__(self, parent)
    
    def double_click_slot(self, index):
        row = index.row()
        url = self.model.item(row, 2).text()
        self.double_clicked.emit(url)

# def get_drives():
#     drives = []
#     bitmask = windll.kernel32.GetLogicalDrives()
#     for letter in string.ascii_uppercase:
#         if bitmask & 1:
#             drives.append(letter)
#         bitmask >>= 1
        
#     return drives