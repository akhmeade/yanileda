# This Python file uses the following encoding: utf-8
import sys
from view.view import GuiView
from presenter.presenter import Presenter
from model.model import Model

from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])

    gui_view = GuiView()
    model = Model()
    presenter = Presenter(gui_view, model)
    gui_view.set_presenter(presenter)


    sys.exit(app.exec_())
