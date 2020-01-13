# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/mainwindow.ui", self)

