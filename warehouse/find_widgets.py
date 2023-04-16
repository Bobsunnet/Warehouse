import sys, os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence

from OperationClasses import ModelCache

import dbConnector as db

BASEDIR = os.path.dirname(__file__)
IMAGES_PATH = os.path.join(BASEDIR, 'static/images')


class FindWidget(QtWidgets.QWidget):
    """
    All events connections must be released in sub-classes!!!
    lnedit_search : Finder
    btn_show_full_table : full table show
    btn_edit_object : editing button
    btn_add_object: adding proper object
    layout_1: lnedit
    layout_2: buttons
    """

    def __init__(self, obj_name:str, table_name:str, headers):
        super().__init__()
        self.db_table_name = table_name
        self.headers = headers
        self.model_cache = ModelCache(self)
        self.common_widgets_setup()
        self.init_ui(obj_name)

    def init_ui(self, obj_name):
        self.setObjectName(obj_name)
        self.setWindowTitle(self.db_table_name.capitalize())
        self.setProperty('findWidget', True)

    def common_widgets_setup(self):
        self.lnedit_search = QtWidgets.QLineEdit()
        self.lnedit_search.setPlaceholderText(f'Enter {self.windowTitle().lower()} name')

        self.btn_show_full_table = QtWidgets.QPushButton(QIcon(QPixmap('static/images/table-grid.png')), ' Show all')
        self.btn_show_full_table.setObjectName('btn_show_full_table')

        self.btn_edit_object = QtWidgets.QPushButton(QIcon(QPixmap('static/images/edit.png')), ' Edit')
        self.btn_edit_object.setObjectName('btn_edit_object')

        self.btn_delete_row = QtWidgets.QPushButton('Delete')
        self.btn_delete_row.setObjectName('btn_delete_row')

        self.btn_add_object = QtWidgets.QPushButton(QIcon(QPixmap('static/images/add.png')), ' Add')
        self.btn_add_object.setObjectName('btn_add_object')

        self.layout_1 = QtWidgets.QHBoxLayout()
        self.layout_1.addWidget(self.lnedit_search)

        self.layout_2 = QtWidgets.QHBoxLayout()
        self.layout_2.addWidget(self.btn_show_full_table)
        self.layout_2.addWidget(self.btn_edit_object)
        self.layout_2.addWidget(self.btn_delete_row)
        self.layout_2.addWidget(self.btn_add_object)

        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.addLayout(self.layout_1)
        self.layout_main.addLayout(self.layout_2)

        self.setLayout(self.layout_main)

    def get_db_table_name(self):
        return self.db_table_name


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = FindWidget('OBJECT', 'TITLELEELEL', db.ClientDB)
    window.show()
    sys.exit(app.exec_())
