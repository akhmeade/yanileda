# This Python file uses the following encoding: utf-8

from pathlib import Path

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtGui import QIcon

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal

from .file_systems import FileSystem
from .file_systems import BublicFileSystem

import resources
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
    download_from_auth_yadisk = pyqtSignal(str, str, dict)
    download_from_bublic_yadisk = pyqtSignal(str, str, dict)
    upload_to_auth_yadisk = pyqtSignal(str, str, dict)
    
    open_link_signal = pyqtSignal()

    local_browse_clicked = pyqtSignal(KeyType, SecurityAlgorithm)
    yadisk_browse_clicked = pyqtSignal(KeyType, SecurityAlgorithm)

    local_algorithm_changed = pyqtSignal(SecurityAlgorithm, KeyType)
    yadisk_algorithm_changed = pyqtSignal(SecurityAlgorithm, KeyType)

    set_media_folder = pyqtSignal(str)

    
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

        self.icon = QIcon(":/img/images/icon.png")
        self.setWindowIcon(self.icon)
    
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
        file_system.algorithm_changed.connect(self.local_algorithm_changed)

        self.local_files.addTab(file_system, "Local file system")
        file_system.set_load_button_enable(False)
    
    def add_authorized_yadisk_tab(self):
        file_system = FileSystem(magic_const.YADISK_FILE_SYSTEM_LABELS, "yadisk_auth")
        file_system.double_clicked.connect(self.get_yadisk_listdir)
        file_system.move_clicked.connect(self.move_file_from_yadisk)
        file_system.browse_clicked.connect(self.yadisk_browse_clicked)
        file_system.algorithm_changed.connect(self.yadisk_algorithm_changed)
        file_system.set_media_folder.connect(self.set_media_folder)
        
        self.yadisk_files.addTab(file_system, "YaDisk")
        self.yadisk_files.setCurrentWidget(file_system)
    
    def add_bublic_yadisk_tab(self, name="name"):
        file_system = BublicFileSystem(magic_const.YADISK_FILE_SYSTEM_LABELS, "bublic")
        file_system.double_clicked.connect(self.get_bublic_listdir)
        file_system.move_clicked.connect(self.move_file_from_bublic_yadisk)
        file_system.algorithm_changed.connect(self.yadisk_algorithm_changed)
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
    
    def get_crypto_data(self, file_system):
        result = {
            "algorithm": file_system.get_algorithm(),
            "key_type": file_system.get_key_type(),
            "key": file_system.get_key().encode("utf-8"),
            "media_path": file_system.get_file_path(),
            "take_file_from_yadisk": file_system.take_file_from_yadisk(),
            "media_type": file_system.get_media_type()
        }
        
        return result

    def move_file_from_yadisk(self):
        local_system = self.get_local_system()
        yadisk_files = self.get_yadisk()
        from_folder = Path(yadisk_files.get_folder_path())
        to_folder = Path(local_system.get_folder_path())
        
        file_name = yadisk_files.get_file_name()
        from_path = from_folder / file_name
        to_path = to_folder / file_name

        encryption_data = self.get_crypto_data(yadisk_files)
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

        encryption_data = self.get_crypto_data(local_system)
        self.upload_to_auth_yadisk.emit(from_path.as_posix(), to_path.as_posix(), encryption_data)
    
    def move_file_from_bublic_yadisk(self):
        local_system = self.get_local_system()
        yadisk_files = self.get_yadisk()

        from_url = yadisk_files.get_folder_path()

        to_folder = Path(local_system.get_folder_path())
        file_name = yadisk_files.get_file_name()

        to_path = to_folder / file_name

        encryption_data = self.get_crypto_data(yadisk_files)
        self.download_from_bublic_yadisk.emit(from_url, to_path.as_posix(), encryption_data)
    
    def get_yadisk_folder_name(self):
        return self.yadisk_files.currentWidget().get_folder_path()
    
    def get_local_folder_name(self):
        return self.local_files.currentWidget().get_folder_path()

    def browse(self, filesystem, result):
        #filesystem.put_key("")
        filesystem.put_file_path("")
        
        if result["action"] == "get_save_filename":
            path = QFileDialog.getSaveFileName(self, "Create file", "new",
                result["limits"])
            filesystem.put_file_path(path[0])
        
        elif result["action"] == "get_open_filename":
            path = QFileDialog.getOpenFileName(self, "Open file", "",
                result["limits"])
            filesystem.put_file_path(path[0])
        else:
            pass

    def local_browse(self, result):
        filesystem = self.get_local_system()
        self.browse(filesystem, result)
    
    def yadisk_browse(self, result):
        filesystem = self.get_yadisk()
        self.browse(filesystem, result)
    
    def put_local_key(self, key):
        filesystem = self.get_local_system()
        filesystem.put_key(key)       
    
    def put_yadisk_key(self, key):
        filesystem = self.get_yadisk()
        filesystem.put_key(key)
    
    def yadisk_tab_changed(self):
        yadisk_filesystem = self.yadisk_files.currentWidget()
        local_filesystem = self.local_files.currentWidget()
        if yadisk_filesystem.system_type == "yadisk_auth":
            local_filesystem.set_load_button_enable(True)
        elif yadisk_filesystem.system_type == "bublic":
            local_filesystem.set_load_button_enable(False)
        else:
            logger.error("In yadisk tab wrong system type")
    def show_progress_dialog(self, message, value=0, minmax=None):
    
        if minmax == None:
            minmax = (0, 0)
        self.progress = QProgressDialog(self)
        self.progress.setWindowTitle("Please, wait")
        self.progress.setLabelText(message)
        self.progress.setRange(*minmax)
        self.progress.setValue(value)
        self.progress.setCancelButton(None)
        self.progress.show()
        
        logger.info("Progress bar is opened")

    def close_progress_dialog(self):
        self.progress.close()
        logger.info("Progress bar is closed")