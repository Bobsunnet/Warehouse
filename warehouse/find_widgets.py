import sys, os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap

from OperationClasses import DataCache, DataHandler

import dbConnector as db

BASEDIR = os.path.dirname(__file__)
IMAGES_PATH = os.path.join(BASEDIR, 'static/images')

class FindWidget(QtWidgets.QWidget):
    '''
    All events connections must be release in sub-classes!!!
    lnedit_search : Finder
    btn_show_full_table : full table show
    btn_edit_object : editing button
    btn_add_object: adding proper object
    layout_1: lnedit
    layout_2: buttons
    '''

    def __init__(self, obj_name, window_title, object_class):
        super().__init__()
        self.setObjectName(obj_name)
        self.setWindowTitle(window_title)
        self.setProperty('findWidget', True)
        # todo нужно сделать отдельный класс для дата кеша и лоадера
        self.data_cache = DataCache()
        self.data_loader = db.DataLoader(object_class)

        self.common_widgets_setup()

    def common_widgets_setup(self):
        self.lnedit_search = QtWidgets.QLineEdit()
        self.lnedit_search.setPlaceholderText(f'Enter {self.windowTitle().lower()} name')

        self.btn_show_full_table = QtWidgets.QPushButton(QIcon(QPixmap('static/images/table-grid.png')), ' Show all')
        self.btn_show_full_table.setObjectName('btn_show_full_table')

        self.btn_edit_object = QtWidgets.QPushButton(QIcon(QPixmap('static/images/edit.png')), ' Edit')
        self.btn_edit_object.setObjectName('btn_edit_object')

        self.btn_add_object = QtWidgets.QPushButton(QIcon(QPixmap('static/images/add.png')), ' Add')
        self.btn_add_object.setObjectName('btn_add_object')

        self.layout_1 = QtWidgets.QHBoxLayout()
        self.layout_1.addWidget(self.lnedit_search)

        self.layout_2 = QtWidgets.QHBoxLayout()
        self.layout_2.addWidget(self.btn_show_full_table)
        self.layout_2.addWidget(self.btn_edit_object)
        self.layout_2.addWidget(self.btn_add_object)

        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.addLayout(self.layout_1)
        self.layout_main.addLayout(self.layout_2)

        self.setLayout(self.layout_main)

    def get_active_model(self):
        return self.data_cache.get_active_model()

    def set_active_model(self, model):
        self.data_cache.set_active_model(model)

    def get_cache_list(self):
        return self.data_cache.get_cache_list()

    def set_cache_list(self, value):
        self.data_cache.set_cache_list(value)





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = FindWidget('OBJECT', 'TITLELEELEL', db.ClientDB)
    window.show()
    sys.exit(app.exec_())
