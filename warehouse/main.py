import sys
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize

# TAB_NAMES = ['Warehouse', 'Rental', 'Client', 'Item', 'Category']

basedir = os.path.dirname(__file__)
path = os.path.join(basedir, 'static/style/styles.css')

with open(path, 'r') as file:
    style = file.read()
    print(style)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.warehouse_widget_setup()
        self.rental_widget_setup()
        self.client_widget_setup()
        self.item_widget_setup()
        self.category_widget_setup()
        self.mainWindow_setup()
        self.layout_setup()

    def mainWindow_setup(self):
        self.setGeometry(200, 150, 800, 600)
        toolbar = QtWidgets.QToolBar('Main toolbar')
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        self.table_widget = QtWidgets.QTableView()
        self.table_widget.setObjectName('table_widget')
        self.table_widget.setStyleSheet(style)

        self.tab_window = QtWidgets.QTabWidget()
        self.tab_window.setObjectName('tab_window')
        self.tab_window.setStyleSheet(style)

        widgets_list = [self.warehouse_widget,self.rental_widget, self.client_widget, self.item_widget, self.category_widget]

        for widg in widgets_list:
            self.tab_window.addTab(widg, widg.windowTitle())

    def layout_setup(self):
        main_layout = QtWidgets.QVBoxLayout()

        bot_layout = QtWidgets.QVBoxLayout()
        bot_layout.addWidget(self.table_widget)

        main_layout.addWidget(self.tab_window)
        main_layout.addLayout(bot_layout)

        main_block_widget = QtWidgets.QWidget()
        main_block_widget.setObjectName('main_block_widget')
        main_block_widget.setStyleSheet(style)
        main_block_widget.setLayout(main_layout)

        self.setCentralWidget(main_block_widget)

    def warehouse_widget_setup(self):
        self.warehouse_widget = QtWidgets.QWidget()
        self.warehouse_widget.setObjectName('warehouse_widget')
        self.warehouse_widget.setWindowTitle('Warehouse')
        self.warehouse_widget.setStyleSheet(style)

    def rental_widget_setup(self):
        self.rental_widget = QtWidgets.QWidget()
        self.rental_widget.setObjectName('rental_widget')
        self.rental_widget.setWindowTitle('Rental')
        self.rental_widget.setStyleSheet(style)

    def client_widget_setup(self):
        self.client_widget = QtWidgets.QWidget()
        self.client_widget.setObjectName('client_widget')
        self.client_widget.setWindowTitle('Client')
        self.client_widget.setStyleSheet(style)

        btn_client_all = QtWidgets.QPushButton('Show all')
        btn_client_all.setObjectName('btn_client_all')
        btn_client_all.setStyleSheet(style)

        btn_client_find = QtWidgets.QPushButton('Show find')
        btn_client_find.setObjectName('btn_client_find')
        btn_client_find.setStyleSheet(style)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(btn_client_all)
        top_layout.addWidget(btn_client_find)

        self.client_widget.setLayout(top_layout)

    def item_widget_setup(self):
        self.item_widget = QtWidgets.QWidget()
        self.item_widget.setObjectName('item_widget')
        self.item_widget.setWindowTitle('Items')
        self.item_widget.setStyleSheet(style)

        btn_all_items = QtWidgets.QPushButton('All items')
        btn_all_items.setStyleSheet(style)
        btn_all_items.setObjectName('btn_all_items')

    def category_widget_setup(self):
        self.category_widget = QtWidgets.QWidget()
        self.category_widget.setObjectName('category_widget')
        self.category_widget.setWindowTitle('Category')
        self.category_widget.setStyleSheet(style)


# *************************** LOGIC **************************************
# *************************** EVENTS/ACTIONS **************************************


# *************************** PASS **************************************


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
