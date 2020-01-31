# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication


from view.view import GuiView
from presenter.presenter import Presenter
from presenter.ipresenter import IPresenter
from model.authorized_yadisk_model import AuthorizedYadiskModel
from model.bublic_yadisk_model import BublicYadiskModel
from model.local_model import LocalModel

if __name__ == "__main__":
    app = QApplication([])

    gui_view = GuiView()
    yadisk_model = AuthorizedYadiskModel()
    local_model = LocalModel()
    bublic_yadisk_model = BublicYadiskModel()
    presenter = Presenter(gui_view, yadisk_model, local_model, bublic_yadisk_model)
    gui_view.set_presenter(presenter)

    sys.exit(app.exec_())
