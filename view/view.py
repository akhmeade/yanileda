# This Python file uses the following encoding: utf-8

from .iview import IView
from .mainwindow import MainWindow

class GuiView(IView):
    """
    Graphical User Interface
    """
    def __init__(self):
        self.mainwindow = MainWindow()
        self.mainwindow.show()
        self.presenter = None

    def connect(self):
        pass

    def send_connection_code(self):
        pass

    def set_presenter(self, presenter):
        self.presenter = presenter
