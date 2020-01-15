# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication


from view.view import GuiView
from presenter.presenter import Presenter
from model.yadisk_model import YadiskModel
from model.local_model import LocalModel

if __name__ == "__main__":
    app = QApplication([])

    gui_view = GuiView()
    yadisk_model = YadiskModel()
    local_model = LocalModel()
    presenter = Presenter(gui_view, yadisk_model, local_model)
    gui_view.set_presenter(presenter)


    sys.exit(app.exec_())
