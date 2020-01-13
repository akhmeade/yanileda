# This Python file uses the following encoding: utf-8
import sys
from view import view
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    gui_view = view.GuiView()
    # window.show()
    sys.exit(app.exec_())
