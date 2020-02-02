# This Python file uses the following encoding: utf-8

from PyQt5.QtCore import QObject

from .iview import IView
from .mainwindow import MainWindow
from .connection_dialog import ConnectionDialog
from .open_link_dialog import OpenLinkDialog

class GuiView(QObject, IView):
    """
    Graphical User Interface
    """
    def __init__(self):
        super().__init__()
        self.mainwindow = MainWindow()
        self.mainwindow.show()
        self.presenter = None
        self.connect_to_actions()

    def connect_to_actions(self):
        self.mainwindow.connect_to_yadisk_signal.connect(self.connect_to_yadisk)
        self.mainwindow.get_local_listdir.connect(self.get_local_listdir)
        self.mainwindow.get_yadisk_listdir.connect(self.get_yadisk_listdir)
        self.mainwindow.get_bublic_listdir.connect(self.get_bublic_listdir)
        self.mainwindow.move_file_signal.connect(self.move_file)
        self.mainwindow.open_link_signal.connect(self.open_link)

    def set_presenter(self, presenter):
        self.presenter = presenter

    def connect_to_yadisk(self):
        self.presenter.connect_to_yadisk()

    def set_verification_url(self, url):
        self.dialog = ConnectionDialog(url)
        self.dialog.accepted.connect(self.send_verification_code)
        self.dialog.show()

    def send_verification_code(self):
        code = self.dialog.get_verification_code()
        self.presenter.verificate_auth(code)

    def set_is_verified(self, is_verified):
        if is_verified:
            self.dialog.close()
            self.mainwindow.show_status("Connected to Yandex Disk")
            self.mainwindow.add_authorized_yadisk_tab()
        else:
            self.dialog.show_warning()

    def get_yadisk_listdir(self, path):
        self.presenter.get_yadisk_listdir(path)

    def get_local_listdir(self, path):
        self.presenter.get_local_listdir(path)

    def show_local_listdir(self, listdir, path):
        self.mainwindow.show_local_listdir(listdir, path)

    def show_yadisk_listdir(self, listdir, path):
        self.mainwindow.show_yadisk_listdir(listdir, path)
    
    def move_file(self, from_file, to_file):
        self.presenter.move_file(from_file, to_file)
        self.update()
    
    def update(self):
        yadisk_folder = self.mainwindow.get_yadisk_folder_name()
        local_folder = self.mainwindow.get_local_folder_name()
        self.get_yadisk_listdir(yadisk_folder)
        self.get_local_listdir(local_folder)
    
    def open_link(self):
        self.dialog = OpenLinkDialog()
        self.dialog.accepted.connect(self.send_bublic_url)
        self.dialog.show()
    
    def send_bublic_url(self):
        url = self.dialog.get_bublic_url()
        self.presenter.open_bublic_url(url)
    
    def set_is_bublic_url_correct(self, is_correct):
        if is_correct:
            self.dialog.close()
            name = self.dialog.get_tab_name()
            self.mainwindow.add_bublic_yadisk_tab(name)
        else:
            self.dialog.show_warning()
    
    def get_bublic_listdir(self, url):
        self.presenter.get_bublic_listdir(url)