import sys
import os

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, QSortFilterProxyModel, Qt, QModelIndex, QRect
from PyQt5.QtGui import QIcon

from TableInterface import TableModel, BaseDelegate, TableWidget
import dbConnector as db
import add_widgets
from find_widgets import FindWidget, DataCache, DataHandler

DEBUG = True
HEADERS_CLIENTS = ['Name', 'Phone', 'Email', '_filter']
HEADERS_CATS = ['Category', '_filter']
HEADERS_RENTALS = ['Event/Rent', 'Client', 'Date', 'Descr', 'Status', '_filter']
HEADERS_ITEMS = ['Item', 'Category', 'Amount', '_filter']

BASEDIR = os.path.dirname(__file__)
STYLES_PATH = os.path.join(BASEDIR, 'static/style/styles.css')

with open(STYLES_PATH, 'r') as file:
    style = file.read()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_handler = DataHandler()
        self.add_rental_window = None
        self.add_client_window = None

        self.active_tab = None
        self.active_cell = None

        self.warehouse_widget_setup()
        self.rental_widget_setup()
        self.client_widget_setup()
        self.item_widget_setup()
        self.category_widget_setup()
        self.mainWindow_setup()
        self.layout_setup()

    def mainWindow_setup(self):
        self.setGeometry(200, 150, 800, 700)
        toolbar = QtWidgets.QToolBar('Main toolbar')
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        self.table_widget = TableWidget()
        self.table_widget.setObjectName('table_widget')

        self.tab_window = QtWidgets.QTabWidget()
        self.tab_window.setObjectName('tab_window')
        self.tab_window.currentChanged.connect(lambda i: self.tab_changed(i))

        act_add_client = QtWidgets.QAction('add_client', self)
        act_add_client.setObjectName('act_add_client')
        act_add_client.triggered.connect(self.act_client_add_clicked)

        act_add_rental = QtWidgets.QAction('add_rent', self)
        act_add_rental.setObjectName('act_add_rent')
        act_add_rental.triggered.connect(self.act_rental_add_clicked)

        act_add_category = QtWidgets.QAction('add_cat', self)
        act_add_category.setObjectName('act_add_cat')
        act_add_category.triggered.connect(self.act_category_add_clicked)

        act_add_item = QtWidgets.QAction('add_item', self)
        act_add_item.setObjectName('act_add_item')
        act_add_item.triggered.connect(self.act_item_add_clicked)

        act_debug_versatile = QtWidgets.QAction(QIcon('static/images/bug_black.png'),'Debug', self)
        act_debug_versatile.triggered.connect(self.debug_versatile)

        toolbar.addAction(act_add_client)
        toolbar.addSeparator()
        toolbar.addAction(act_add_rental)
        toolbar.addSeparator()
        toolbar.addAction(act_add_category)
        toolbar.addSeparator()
        toolbar.addAction(act_add_item)
        toolbar.addSeparator()
        toolbar.addAction(act_debug_versatile)

        widgets_list = [self.warehouse_widget, self.rental_widget, self.client_widget, self.item_widget,
                        self.category_widget]

        for w in widgets_list:
            self.tab_window.addTab(w, w.windowTitle())

    def layout_setup(self):
        main_layout = QtWidgets.QVBoxLayout()

        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.tab_window)
        splitter.addWidget(self.table_widget)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([125, 150])
        main_layout.addWidget(splitter)

        main_block_widget = QtWidgets.QWidget()
        main_block_widget.setObjectName('main_block_widget')

        main_block_widget.setLayout(main_layout)

        self.setCentralWidget(main_block_widget)

    def warehouse_widget_setup(self):
        self.warehouse_widget = QtWidgets.QWidget()
        self.warehouse_widget.setObjectName('warehouse_widget')
        self.warehouse_widget.setWindowTitle('Warehouse')

    def rental_widget_setup(self):
        self.rental_widget = FindWidget('rental_widget','Rental', db.RentalDB)
        self.rental_widget.headers = HEADERS_RENTALS

        self.rental_widget.checkbox_status = QtWidgets.QCheckBox('Show Ended')
        self.rental_widget.layout_1.addWidget(self.rental_widget.checkbox_status)

        self.rental_widget.checkbox_status.clicked.connect(self.checkbox_status_clicked)
        self.rental_widget.btn_add_object.clicked.connect(self.act_rental_add_clicked)
        self.rental_widget.btn_edit_object.clicked.connect(self.btn_edit_rental_clicked)
        self.rental_widget.btn_show_full_table.clicked.connect(self.btn_show_full_rental_clicked)

        self.add_rental_window = add_widgets.RentalAddWindow('add_rental_window','Rental')

    def client_widget_setup(self):
        self.client_widget = FindWidget('client_widget', 'Client', db.ClientDB)
        self.client_widget.headers = HEADERS_CLIENTS

        self.client_widget.btn_add_object.clicked.connect(self.act_client_add_clicked)
        self.client_widget.btn_edit_object.clicked.connect(self.btn_edit_client_clicked)
        self.client_widget.btn_show_full_table.clicked.connect(self.btn_show_full_clients_clicked)

        self.add_client_window = add_widgets.ClientAddWindow('add_client_window', 'Client')

    def item_widget_setup(self):
        self.item_widget = FindWidget('item_widget', 'Items', db.ItemDB)
        self.item_widget.headers = HEADERS_ITEMS

        self.item_widget.btn_add_object.clicked.connect(self.act_item_add_clicked)
        self.item_widget.btn_edit_object.clicked.connect(self.btn_edit_items_clicked)
        self.item_widget.btn_show_full_table.clicked.connect(self.btn_show_full_items_clicked)

        self.add_item_window = add_widgets.ItemAddWindow('add_item_window','Item')

    def category_widget_setup(self):
        self.category_widget = FindWidget('category_widget', 'Category', db.CategoryDB)
        self.category_widget.headers = HEADERS_CATS

        self.category_widget.btn_add_object.clicked.connect(self.act_category_add_clicked)
        self.category_widget.btn_edit_object.clicked.connect(self.btn_edit_category_clicked)
        self.category_widget.btn_show_full_table.clicked.connect(self.btn_show_full_category_clicked)

        self.add_category_window = add_widgets.CategoryAddWindow('add_category_window','Category')

# ************************************************* LOGIC *********************************************************
    def debug_versatile(self):
        # self.action_show_full_table()
        print('Debug is not connected now')

    # *************************** EVENTS/ACTIONS **************************************
    def tab_changed(self, i):
        self.active_tab = self.tab_window.currentWidget()
        # if i != 0:
        #     self.action_show_full_table()

    def checkbox_status_clicked(self):
        # TODO переделать логику чтобы не быть привязаным к отдельной функции
        self.action_show_all_rentals()
        self.hide_ended_events()


    def btn_show_full_category_clicked(self):
        self.action_show_full_table(self.make_table_category)

    def btn_edit_category_clicked(self):
        res = self.category_widget.data_cache.get_active_sell()
        print(type(res), res)

    def act_category_add_clicked(self):
        self.add_category_window.show()


    def btn_show_full_clients_clicked(self):
        self.action_show_full_table(self.make_table_clients)

    def btn_edit_client_clicked(self):
        print(f'editing: {self.client_widget.data_cache.get_active_sell()}')

    def act_client_add_clicked(self):
        self.add_client_window.show()


    def btn_show_full_rental_clicked(self):
        self.action_show_full_table(self.make_table_rentals)

    def btn_edit_rental_clicked(self):
        res = self.rental_widget.data_cache.get_active_sell()
        print(type(res), res)

    def act_rental_add_clicked(self):
        self.add_rental_window.show()


    def btn_show_full_items_clicked(self):
        self.action_show_full_table(self.make_table_items)

    def btn_edit_items_clicked(self):
        print(self.item_widget.data_cache.get_active_sell())

    def act_item_add_clicked(self):
        self.add_item_window.show()

    # ***************************** ACTIONS **************************************
    def action_show_full_table(self, table_convert_func):
        widget = self.tab_window.currentWidget()
        if not widget.get_active_model():  # Здесь он ругается на вкладку Warehouse так как это QWidget, а не FindWidget
            data = widget.data_loader.load_all()
            print('Connection USED')
            model = self.make_model(data, widget.headers, table_convert_func,
                                widget.lnedit_search)
            widget.set_active_model(model)
        self.draw_table(widget.get_active_model(), widget)

    # ОСТАТОК ВРЕМЕННЫЙ
    def action_show_all_rentals(self):
        widget = self.rental_widget
        if not widget.data_cache.get_cache_list():
            data = widget.data_loader.load_all()
            widget.data_cache.set_cache_list(data)
            print('connection')
        model = self.make_model(widget.data_cache.get_cache_list(), HEADERS_RENTALS, self.make_table_rentals,
                                widget.lnedit_search)
        self.draw_table(model, widget)

    # *************************** FUNCTIONS **************************************
    @staticmethod
    def make_model(obj_lst, headers, table_func, lnedit):
        '''Make a model for proper table

        :param obj_lst: List of ORM objects
        :param headers: Header for model
        :param table_func: Func-converter for table
        :param lnedit: LineEdit connected to type of table
        :return: model with connected filter
        '''
        table = table_func(obj_lst)
        model = TableModel(table, headers)
        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(model.columnCount() - 1)

        lnedit.textChanged.connect(filter_proxy_model.setFilterRegExp)
        return filter_proxy_model

    # @staticmethod
    def make_table_rentals(self, rentals: list):
        if self.rental_widget.checkbox_status.isChecked():
            table = [[rent, rent.Client, rent.rental_date, rent.details, rent.rental_status, rent.rental_name] for rent
                     in rentals]
        else:
            table = [[rent, rent.Client, rent.rental_date, rent.details, rent.rental_status, rent.rental_name] for rent
                     in rentals if rent.rental_status]
        return table

    @staticmethod
    def make_table_items(items: list):
        table = [[item, item.Category, item.amount, item.item_name] for item in items]
        return table

    @staticmethod
    def make_table_category(cats: list):
        table = [[cat, cat.category_name] for cat in cats]
        return table

    @staticmethod
    def make_table_clients(clients: list):
        table = [[client, client.phone_number, client.email, client.client_name] for client in clients]
        return table

    def hide_ended_events(self):
        print('HIDING ENDED EVENTS')

    def draw_table(self, model, widget):
        self.table_widget.setModel(model)
        self.table_widget.setItemDelegate(BaseDelegate())
        self.table_widget.selectionModel().currentChanged.connect(lambda x: widget.data_cache.set_active_sell(x.data()))
        self.table_widget.selectionModel().currentChanged.connect(self.cell_highlighted)

        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.table_widget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        filtered_column = model.columnCount()-1
        self.table_widget.setFilterColumn(filtered_column)

    def cell_highlighted(self, current, previous):
        current_row, current_col = current.row(), current.column()
        model = self.table_widget.model()
        print(model.itemData(current).get(0))
        # print(current_row, current_col)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(style)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
