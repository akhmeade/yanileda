# This Python file uses the following encoding: utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QProgressDialog

from .iview import IView
from .mainwindow import MainWindow
from .connection_dialog import ConnectionDialog
from .open_link_dialog import OpenLinkDialog

import magic_const
import time
import logging
logger = logging.getLogger(__name__)

class Progress(QThread):
    # def __init__(self, parent):
    #     super(QThread, self).__init__()
    #     self.p = parent

    def run(self):
        logger.info("do work")
        for i in range(100):
            logger.info(i)
            time.sleep(1)
        self.progress = QProgressDialog()
        self.progress.setWindowTitle("Please, wait")
        self.progress.setLabelText("message")
        self.progress.setRange(0, 0)
        self.progress.setValue(0)
        self.progress.setCancelButton(None)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.exec_()

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
        
        # download/upload files
        self.mainwindow.download_from_auth_yadisk.connect(self.download_from_auth_yadisk)
        self.mainwindow.download_from_bublic_yadisk.connect(self.download_from_bublic_yadisk)
        self.mainwindow.upload_to_auth_yadisk.connect(self.upload_to_auth_yadisk)
        
        # add new tab
        self.mainwindow.open_link_signal.connect(self.open_link)

        #browse clicked
        self.mainwindow.local_browse_clicked.connect(self.local_browse_request)
        self.mainwindow.yadisk_browse_clicked.connect(self.yadisk_browse_request)
        #self.mainwindow.yadisk_browse_clicked.connect(self.browse)

        self.mainwindow.local_algorithm_changed.connect(self.on_local_algorithm_changed)
        self.mainwindow.yadisk_algorithm_changed.connect(self.on_yadisk_algorithm_changed)

        self.mainwindow.set_media_folder.connect(self.on_set_media_folder)

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
    
    def show_error(self, message):
        self.msg_box = QMessageBox(QMessageBox.Warning, "Warning", message)
        self.msg_box.show()
    
    # def _show(self):
    #     self.progress = QProgressDialog()
    #     self.progress.setWindowTitle("Please, wait")
    #     self.progress.setLabelText("aSDASD")
    #     self.progress.setRange(0,0)
    #     self.progress.setValue(0)
    #     self.progress.setCancelButton(None)
    

    def show_progress_dialog(self, message, value=0, minmax=None):
        #self.progress = Progress(self.mainwindow)
        #logger.info("Thread run")
        #self.progress.start()
        #logger.info("Progress bar is opened")
        if minmax == None:
            minmax = (0, 0)
        self.progress = QProgressDialog()
        self.progress.setWindowTitle("Please, wait")
        self.progress.setLabelText(message)
        self.progress.setRange(*minmax)
        self.progress.setValue(value)
        self.progress.setCancelButton(None)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.exec_()
        
        # self.progress = Progress()
        
        # self.thread = QThread()
        # self.progress.moveToThread(self.thread)
        # #self.progress.moveToThread(self.thread)
        # self.thread.started.connect(self.progress.do_work)
        # self.thread.finished.connect(self.progress.close)
        # self.thread.start()
        # #logger.info("Thread run")
        # #self.thread.run()
        # logger.info("Progress bar is opened")



    def close_progress_dialog(self):
        #return
        #return
        #self.progress.terminate()
        logger.info("Progress bar is closed")
        #self.thread.quit()
        self.progress.close()

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
    
    def download_from_auth_yadisk(self, from_file, to_file, encryption_data):
        self.presenter.download_from_auth_yadisk(from_file, to_file, encryption_data)
        self.update_local()
    
    def download_from_bublic_yadisk(self, from_file, to_file, encryption_data):
        self.presenter.download_from_bublic_yadisk(from_file, to_file, encryption_data)
        self.update_local()
    
    def upload_to_auth_yadisk(self, from_file, to_file, encryption_data):
        self.presenter.upload_to_auth_yadisk(from_file, to_file, encryption_data)
        self.update_auth_yadisk()
        self.update_local()
    
    def update_local(self):
        local_folder = self.mainwindow.get_local_folder_name()
        self.get_local_listdir(local_folder)
    
    def update_auth_yadisk(self):
        yadisk_folder = self.mainwindow.get_yadisk_folder_name()
        self.get_yadisk_listdir(yadisk_folder)
    
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
    
    def local_browse_request(self, key_type, algorithm):
        self.presenter.local_browse(key_type, algorithm)
    
    def yadisk_browse_request(self, key_type, algorithm):
        self.presenter.yadisk_browse(key_type, algorithm)
    
    def local_browse(self, result):
        self.mainwindow.local_browse(result)
    
    def yadisk_browse(self, result):
        self.mainwindow.yadisk_browse(result)
    
    def on_local_algorithm_changed(self, algorithm, key_type):
        self.presenter.get_local_key(algorithm, key_type)

    def on_yadisk_algorithm_changed(self, algorithm, key_type):
        self.presenter.get_yadisk_key(algorithm, key_type)
    
    def put_local_key(self, key):
        self.mainwindow.put_local_key(key)
    
    def put_yadisk_key(self, key):
        self.mainwindow.put_yadisk_key(key)
    
    def on_set_media_folder(self, path):
        self.presenter.set_media_folder(path)