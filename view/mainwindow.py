# This Python file uses the following encoding: utf-8

from pathlib import Path

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFileDialog

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal

from .file_systems import FileSystem
from .file_systems import BublicFileSystem

import magic_const
from magic_const import KeyType
from magic_const import SecurityAlgorithm

import logging
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):

    connect_to_yadisk_signal = pyqtSignal()
    get_yadisk_listdir = pyqtSignal(str)
    get_local_listdir = pyqtSignal(str)
    get_bublic_listdir = pyqtSignal(str)
    
    move_file_signal = pyqtSignal(str, str)
    download_from_auth_yadisk = pyqtSignal(str, str, tuple)
    download_from_bublic_yadisk = pyqtSignal(str, str, tuple)
    upload_to_auth_yadisk = pyqtSignal(str, str, tuple)
    
    open_link_signal = pyqtSignal()

    local_browse_clicked = pyqtSignal(KeyType, SecurityAlgorithm)
    yadisk_browse_clicked = pyqtSignal(KeyType, SecurityAlgorithm)

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("forms/mainwindow.ui", self)
        self.local_files = QTabWidget()#FileSystem()
        self.add_local_file_system()
        
        self.yadisk_files = QTabWidget()
        
        self.h_layout.layout().addWidget(self.local_files)
        self.h_layout.layout().addWidget(self.yadisk_files)
        
        self.connect_to_actions()
        self.show_status("Not connected")
        self.local_files.show()
    
    def connect_to_actions(self):
        self.connect_to_yadisk_action.triggered.connect(self.connect_to_yadisk)
        self.open_link_action.triggered.connect(self.open_link)
        self.yadisk_files.currentChanged.connect(self.yadisk_tab_changed)
    
    def get_local_system(self):
        return self.local_files.currentWidget()
    
    def get_yadisk(self):
        return self.yadisk_files.currentWidget()

    def add_local_file_system(self):
        file_system = FileSystem(magic_const.LOCAL_FILE_SYSTEM_LABELS, "local")
        
        file_system.double_clicked.connect(self.get_local_listdir)
        file_system.move_clicked.connect(self.move_file_from_local)
        file_system.browse_clicked.connect(self.local_browse_clicked)

        self.local_files.addTab(file_system, "Local file system")
        file_system.set_load_button_enable(False)
    
    def add_authorized_yadisk_tab(self):
        file_system = FileSystem(magic_const.YADISK_FILE_SYSTEM_LABELS, "yadisk_auth")
        file_system.double_clicked.connect(self.get_yadisk_listdir)
        file_system.move_clicked.connect(self.move_file_from_yadisk)
        file_system.browse_clicked.connect(self.yadisk_browse_clicked)
        
        self.yadisk_files.addTab(file_system, "YaDisk")
        self.yadisk_files.setCurrentWidget(file_system)
    
    def add_bublic_yadisk_tab(self, name="name"):
        file_system = BublicFileSystem(magic_const.YADISK_FILE_SYSTEM_LABELS, "bublic")
        file_system.double_clicked.connect(self.get_bublic_listdir)
        file_system.move_clicked.connect(self.move_file_from_bublic_yadisk)
        self.yadisk_files.addTab(file_system, name)
        self.yadisk_files.setCurrentWidget(file_system)

    def connect_to_yadisk(self):
        self.connect_to_yadisk_signal.emit()
        #self.yadisk_files.addTab(FileSystem(), "name")
        #self.connect_to_yadisk_signal.emit()
    
    def open_link(self):
        #self.add_yadisk_tab()
        self.open_link_signal.emit()

    def show_status(self, message):
        self.statusBar().showMessage(message)

    def show_local_listdir(self, listdir, path):
        #print("show local listdir", path)
        self.get_local_system().show_listdir(listdir, path)

    def show_yadisk_listdir(self, listdir, path):
        self.get_yadisk().show_listdir(listdir, path)
    
    def move_file_from_yadisk(self):
        local_system = self.get_local_system()
        yadisk_files = self.get_yadisk()
        from_folder = Path(yadisk_files.get_folder_path())
        to_folder = Path(local_system.get_folder_path())
        
        file_name = yadisk_files.get_file_name()
        from_path = from_folder / file_name
        to_path = to_folder / file_name

        encryption_data = (yadisk_files.get_algorithm(), yadisk_files.get_key_type(), \
            yadisk_files.get_key().encode("utf-8"), yadisk_files.get_file_path())
        self.download_from_auth_yadisk.emit(from_path.as_posix(), to_path.as_posix(), encryption_data)
        #self.move_file_signal.emit(from_path.as_posix(), to_path.as_posix())

    def move_file_from_local(self):
        # TODO : add algorithm and key type

        local_system = self.get_local_system()
        yadisk_files = self.get_yadisk()

        from_folder = Path(local_system.get_folder_path())
        to_folder = Path(yadisk_files.get_folder_path())
        
        file_name = local_system.get_file_name()
        from_path = from_folder / file_name
        to_path = to_folder  / file_name

        encryption_data = (local_system.get_algorithm(), local_system.get_key_type(), \
            local_system.get_key().encode("utf-8"), local_system.get_file_path())
        self.upload_to_auth_yadisk.emit(from_path.as_posix(), to_path.as_posix(), encryption_data)
    
    def move_file_from_bublic_yadisk(self):
        local_system = self.get_local_system()
        yadisk_files = self.get_yadisk()

        from_url = yadisk_files.get_folder_path()

        to_folder = Path(local_system.get_folder_path())
        file_name = yadisk_files.get_file_name()

        to_path = to_folder / file_name

        encryption_data = (yadisk_files.get_algorithm(), yadisk_files.get_key_type(), \
            yadisk_files.get_key().encode("utf-8"), yadisk_files.get_file_path())
        self.download_from_bublic_yadisk.emit(from_url, to_path.as_posix(), encryption_data)
    
    def get_yadisk_folder_name(self):
        return self.yadisk_files.currentWidget().get_folder_path()
    
    def get_local_folder_name(self):
        return self.local_files.currentWidget().get_folder_path()

    def local_browse(self, result):
        filesystem = self.get_local_system()
        
        filesystem.put_key("")
        filesystem.put_file_path("")

        if result["action"] == "show":
            filesystem.put_key(result["key"])
        
        elif result["action"] == "get_save_filename":
            path = QFileDialog.getSaveFileName(self, "Create file", "new",
                result["limits"])
            filesystem.put_file_path(path[0])
        
        elif result["action"] == "get_open_filename":
            path = QFileDialog.getOpenFileName(self, "Open file", "",
                result["limits"])
            filesystem.put_file_path(path[0])
        else:
            pass
    
    def yadisk_tab_changed(self):
        yadisk_filesystem = self.yadisk_files.currentWidget()
        local_filesystem = self.local_files.currentWidget()
        if yadisk_filesystem.system_type == "yadisk_auth":
            local_filesystem.set_load_button_enable(True)
        elif yadisk_filesystem.system_type == "bublic":
            local_filesystem.set_load_button_enable(False)
        else:
            logger.error("In yadisk tab wrong system type")