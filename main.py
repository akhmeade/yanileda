# This Python file uses the following encoding: utf-8
import sys
from view import mainwindow
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    window = mainwindow.MainWindow()
    # window.show()
    sys.exit(app.exec_())
