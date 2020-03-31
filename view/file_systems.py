# This Python file uses the following encoding: utf-8

from pathlib import Path

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction

from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

import magic_const
from magic_const import KeyType


import resources

class FileSystem(QWidget):
    double_clicked = pyqtSignal(str)
    move_clicked = pyqtSignal()
    browse_clicked = pyqtSignal(magic_const.KeyType)

    def __init__(self, label_names, system_type, parent=None):
        """[summary]
        
        Arguments:
            label_names {[type]} -- [description]
            system_type {str} -- [local/yadisk_auth/bublic]
        
        Keyword Arguments:
            parent {[type]} -- [description] (default: {None})
        """
        QWidget.__init__(self, parent)
        uic.loadUi("forms/file_system.ui", self)
        #self.file_system_name.setText(file_system_name)
        self.connect_to_actions()
        self.model = None
        self.protocol = []
        self.system_type = system_type

        self.folder_icon = QIcon(":/img/images/folder_icon.png")
        self.file_icon = QIcon(":/img/images/file_icon.png")

        self.set_label_names(label_names)

        self.fill_combobox(self.algorithms_box, list(magic_const.SecurityAlgorithm))
        self.fill_combobox(self.key_type_box, label_names["key_type"])

        self.key_type_box.currentIndexChanged.connect(self.key_type_changed)

        self.key_type_changed()

        if self.system_type == "yadisk_auth":
            self.listdir.setContextMenuPolicy(Qt.CustomContextMenu)
            self.listdir.customContextMenuRequested.connect(self.show_context_menu)

    def connect_to_actions(self):
        self.listdir.doubleClicked.connect(self.double_click_slot)
        self.path_box.editingFinished.connect(self.get_listdir)
        self.back_button.clicked.connect(self.get_previous_folder)
        self.load_button.clicked.connect(self.move_clicked)
        self.browse_button.clicked.connect(self.browse_slot)
        self.from_yadisk_button.toggled.connect(self.from_yadisk_button_toggled)
    
    def set_label_names(self, label_names):
        self.message_label.setText(label_names["message_label"])
        self.algorithm_label.setText(label_names["algorithm_label"])
        self.key_type_label.setText(label_names["key_type_label"])
        self.load_button.setText(label_names["load_button"])
    
    def fill_combobox(self, combobox, items):
        add_item = lambda item: combobox.addItem(item.value, item)
        list(map(add_item, items))

    def show_listdir(self, listdir, path):
        header = listdir[0]
        listdir = listdir[1:]
        self.listdir_info = listdir.copy()
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
    
    def get_selected_row(self):
        selected = self.listdir.selectedIndexes()
        if len(selected) < 1:
            print("BAD SELECTED")
        selected = selected[1]
        row = selected.row()
        return row

    def set_as_media_folder(self):
        print("triggereddd")

    def show_context_menu(self, pos):
            #print(pos, self.listdir.mapToGlobal(pos), 
        row = self.get_selected_row()
        #print(self.listdir_info[row - 1][1])
        if self.listdir_info[row - 1][0] == "dir":
            self.menu = QMenu(self)
            set_folder = QAction("Set as media folder")
            set_folder.triggered.connect(self.set_as_media_folder)
            self.menu.addAction(set_folder)
            self.menu.exec_(self.listdir.mapToGlobal(pos))
    def key_type_changed(self):
        key_type = self.get_key_type()

        if key_type == KeyType.new_symbols:
            self.key_label.setVisible(True)
            self.key_box.setVisible(True)
            self.path_label.setVisible(False)
            self.file_path_box.setVisible(False)
            self.browse_button.setVisible(False)
            self.from_yadisk_button.setVisible(False)
            self.browse_slot()
        elif key_type == KeyType.existing_symbols:
            self.key_label.setVisible(True)
            self.key_box.setVisible(True)
            self.path_label.setVisible(False)
            self.file_path_box.setVisible(False)
            self.browse_button.setVisible(False)
            self.from_yadisk_button.setVisible(False)
            self.key_box.clear()
        elif key_type == KeyType.new_binary:
            self.key_label.setVisible(False)
            self.key_box.setVisible(False)
            self.path_label.setVisible(True)
            self.file_path_box.setVisible(True)
            self.browse_button.setVisible(True)
            self.from_yadisk_button.setVisible(False)
            self.file_path_box.clear()
        elif key_type == KeyType.existing_binary:
            self.key_label.setVisible(False)
            self.key_box.setVisible(False)
            self.path_label.setVisible(True)
            self.file_path_box.setVisible(True)
            self.browse_button.setVisible(True)
            self.from_yadisk_button.setVisible(False)
            self.file_path_box.clear()
        elif key_type == KeyType.new_media:
            self.key_label.setVisible(True)
            self.key_box.setVisible(True)
            self.path_label.setVisible(True)
            self.file_path_box.setVisible(True)
            self.browse_button.setVisible(True)
            self.from_yadisk_button.setVisible(False)
            self.key_box.clear()
            self.file_path_box.clear()
        elif key_type == KeyType.existing_media:
            self.key_label.setVisible(True)
            self.key_box.setVisible(True)
            self.path_label.setVisible(True)
            self.file_path_box.setVisible(True)
            #self.browse_button.setVisible(True) processed in function below
            self.from_yadisk_button.setVisible(True)
            self.from_yadisk_button_toggled(self.from_yadisk_button.isChecked())
            self.key_box.clear()
            self.file_path_box.clear()
    
    def from_yadisk_button_toggled(self, from_yadisk):
        if from_yadisk:
            self.browse_button.setVisible(False)
        else:
            self.browse_button.setVisible(True)
        

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
    
    def get_key_type(self):
        return self.key_type_box.currentData()

    def browse_slot(self):
        self.browse_clicked.emit(self.get_key_type())
    
    def put_key(self, result):
        self.key_box.setText(result)

class BublicFileSystem(FileSystem):
    def __init__(self, system_type,  parent=None):
        FileSystem.__init__(self, system_type, parent)
    
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