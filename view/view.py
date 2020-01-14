# This Python file uses the following encoding: utf-8

from PyQt5.QtCore import QObject

from .iview import IView
from .mainwindow import MainWindow


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

    def connect_to_yadisk(self):
        self.presenter.connect_to_yadisk()

    def set_verification_url(self, url):
        self.mainwindow.open_connection_dialog(url)

    def send_connection_code(self):
        pass

    def set_presenter(self, presenter):
        self.presenter = presenter
