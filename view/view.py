# This Python file uses the following encoding: utf-8

from PyQt5.QtCore import QObject

from .iview import IView
from .mainwindow import MainWindow
from .connection_dialog import ConnectionDialog

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

    def set_presenter(self, presenter):
        self.presenter = presenter

    def connect_to_yadisk(self):
        self.presenter.connect_to_yadisk()

    def set_verification_url(self, url):
        self.dialog = ConnectionDialog(url)
        self.dialog.accepted.connect(self.send_verification_code)
        self.dialog.show()

    def send_verification_code(self):
        code = self.dialog.code_box.toPlainText()
        self.presenter.verificate_auth(code)

    def set_is_verified(self, is_verified):
        if is_verified:
            self.dialog.close()
            self.mainwindow.show_status("Connected to Yandex Disk")
        else:
            self.dialog.show_warning()

    def show_local_listdir(self, listdir, path):
        self.mainwindow.show_local_listdir(listdir, path)

    def show_yadisk_listdir(self, listdir, path):
        self.mainwindow.show_yadisk_listdir(listdir, path)


