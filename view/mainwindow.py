# This Python file uses the following encoding: utf-8

from pathlib import Path

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal

from .file_systems import FileSystem

class MainWindow(QMainWindow):

    connect_to_yadisk_signal = pyqtSignal()
    get_yadisk_listdir = pyqtSignal(str)
    get_local_listdir = pyqtSignal(str)
    move_file_signal = pyqtSignal(str, str)
    open_link_signal = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("forms/mainwindow.ui", self)
        self.local_files = QTabWidget()#FileSystem()
        self.add_local_file_system()
        
        self.yadisk_files = QTabWidget()
        
        self.h_layout.addWidget(self.local_files)
        self.h_layout.addWidget(self.yadisk_files)
        
        self.connect_to_actions()
        self.show_status("Not connected")
        self.local_files.show()
    
    def get_local_system(self):
        return self.local_files.currentWidget()
    def get_yadisk(self):
        return self.yadisk_files.currentWidget()

    def add_local_file_system(self):
        file_system = FileSystem()
        
        file_system.double_clicked.connect(self.get_local_listdir)
        file_system.move_clicked.connect(self.move_file_from_local)

        self.local_files.addTab(file_system, "Local file system")
    
    def add_cloud_file_system(self, name):
        file_system = FileSystem()
        self.yadisk_files.addTab(file_system, name)

    def connect_to_actions(self):
        self.connect_to_yadisk_action.triggered.connect(self.connect_to_yadisk)
        self.open_link_action.triggered.connect(self.open_link)

    def connect_to_yadisk(self):
        self.connect_to_yadisk_signal.emit()
        #self.yadisk_files.addTab(FileSystem(), "name")
        #self.connect_to_yadisk_signal.emit()
    
    def add_yadisk_tab(self):
        file_system = FileSystem()
        file_system.double_clicked.connect(self.get_yadisk_listdir)
        file_system.move_clicked.connect(self.move_file_from_yadisk)
        self.yadisk_files.addTab(file_system, "YaDisk")
        self.yadisk_files.setCurrentWidget(file_system)
    
    def open_link(self):
        self.add_yadisk_tab()
        self.open_link_signal.emit()

    def show_status(self, message):
        self.statusBar().showMessage(message)

    def show_local_listdir(self, listdir, path):
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
        self.move_file_signal.emit(from_path.as_posix(), to_path.as_posix())


    def move_file_from_local(self):
        local_system = self.get_local_system()
        yadisk_files = self.get_yadisk()

        from_folder = Path(local_system.get_folder_path())
        to_folder = Path(yadisk_files.get_folder_path())
        
        file_name = local_system.get_file_name()
        from_path = from_folder / file_name
        to_path = to_folder  / file_name
        self.move_file_signal.emit(from_path.as_posix(), to_path.as_posix())
    
    def get_yadisk_folder_name(self):
        return self.yadisk_files.currentWidget().get_folder_path()
    
    def get_local_folder_name(self):
        return self.local_files.currentWidget().get_folder_path()