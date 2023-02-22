import sys
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, QSortFilterProxyModel, Qt


from TableInterface import TableModel, BaseDelegate
import dbConnector as db
import add_widgets

# TAB_NAMES = ['Warehouse', 'Rental', 'Client', 'Item', 'Category']
HEADERS_CLIENTS = ['Name', 'phone', 'email', '']
HEADERS_CATS = ['Cat name', '']
HEADERS_RENTALS = ['Name', 'Client', 'Date', 'Descr', 'Status','']

BASEDIR = os.path.dirname(__file__)
STYLES_PATH = os.path.join(BASEDIR, 'static/style/styles.css')


with open(STYLES_PATH, 'r') as file:
    style = file.read()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.add_rental_window = None
        self.add_client_window = None

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

        self.table_widget = QtWidgets.QTableView()
        self.table_widget.setObjectName('table_widget')

        self.tab_window = QtWidgets.QTabWidget()
        self.tab_window.setObjectName('tab_window')

        act_add_client = QtWidgets.QAction('add_client', self)
        act_add_client.setObjectName('act_add_client')
        act_add_client.triggered.connect(self.act_client_add_clicked)

        act_add_rental = QtWidgets.QAction('add_rent', self)
        act_add_rental.setObjectName('act_add_rent')
        act_add_rental.triggered.connect(self.act_rental_add_clicked)

        act_add_category = QtWidgets.QAction('add_cat', self)
        act_add_category.setObjectName('act_add_cat')
        act_add_category.triggered.connect(self.act_category_add_clicked)

        toolbar.addAction(act_add_client)
        toolbar.addSeparator()
        toolbar.addAction(act_add_rental)
        toolbar.addSeparator()
        toolbar.addAction(act_add_category)


        widgets_list = [self.warehouse_widget, self.rental_widget, self.client_widget, self.item_widget,
                        self.category_widget]

        for w in widgets_list:
            self.tab_window.addTab(w, w.windowTitle())



    def layout_setup(self):
        main_layout = QtWidgets.QVBoxLayout()

        bot_layout = QtWidgets.QVBoxLayout()
        bot_layout.addWidget(self.table_widget)

        main_layout.addWidget(self.tab_window)
        main_layout.addLayout(bot_layout)

        main_block_widget = QtWidgets.QWidget()
        main_block_widget.setObjectName('main_block_widget')

        main_block_widget.setLayout(main_layout)

        self.setCentralWidget(main_block_widget)

    def warehouse_widget_setup(self):
        self.warehouse_widget = QtWidgets.QWidget()
        self.warehouse_widget.setObjectName('warehouse_widget')
        self.warehouse_widget.setWindowTitle('Warehouse')

    def rental_widget_setup(self):
        self.rental_widget = QtWidgets.QWidget()
        self.rental_widget.setObjectName('rental_widget')
        self.rental_widget.setWindowTitle('Rental')

        self.lnedit_rental = QtWidgets.QLineEdit()
        self.lnedit_rental.setPlaceholderText('enter rental name')

        self.checkbox_status = QtWidgets.QCheckBox('Show Ended')
        self.checkbox_status.clicked.connect(self.checkbox_status_clicked)

        btn_rental_all = QtWidgets.QPushButton('Show all')
        btn_rental_all.setObjectName('btn_rental_all')
        btn_rental_all.clicked.connect(self.btn_rental_all_clicked)

        btn_rental_find = QtWidgets.QPushButton('Show find')
        btn_rental_find.setObjectName('btn_rental_find')
        btn_rental_find.clicked.connect(self.btn_rental_find_clicked)

        btn_rental_add = QtWidgets.QPushButton('Add')
        btn_rental_add.setObjectName('btn_rental_add')
        btn_rental_add.clicked.connect(self.act_rental_add_clicked)

        layout_1 = QtWidgets.QHBoxLayout()
        layout_1.addWidget(self.lnedit_rental)
        layout_1.addWidget(self.checkbox_status)

        layout_2 = QtWidgets.QHBoxLayout()
        layout_2.addWidget(btn_rental_all)
        layout_2.addWidget(btn_rental_find)
        layout_2.addWidget(btn_rental_add)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_1)
        layout_main.addLayout(layout_2)

        self.rental_widget.setLayout(layout_main)

        self.add_rental_window = add_widgets.RentalAddWindow()

    def client_widget_setup(self):
        self.client_widget = QtWidgets.QWidget()
        self.client_widget.setObjectName('client_widget')
        self.client_widget.setWindowTitle('Client')

        self.lnedit_client = QtWidgets.QLineEdit()
        self.lnedit_client.setPlaceholderText('enter client name or phone')

        btn_client_all = QtWidgets.QPushButton('Show all')
        btn_client_all.setObjectName('btn_client_all')
        btn_client_all.clicked.connect(self.btn_client_all_clicked)

        btn_client_find = QtWidgets.QPushButton('Show find')
        btn_client_find.setObjectName('btn_client_find')
        btn_client_find.clicked.connect(self.btn_client_find_clicked)

        btn_client_add = QtWidgets.QPushButton('Add')
        btn_client_add.setObjectName('btn_client_add')
        btn_client_add.clicked.connect(self.act_client_add_clicked)

        layout_1 = QtWidgets.QHBoxLayout()
        layout_1.addWidget(self.lnedit_client)

        layout_2 = QtWidgets.QHBoxLayout()
        layout_2.addWidget(btn_client_all)
        layout_2.addWidget(btn_client_find)
        layout_2.addWidget(btn_client_add)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_1)
        layout_main.addLayout(layout_2)

        self.client_widget.setLayout(layout_main)

        self.add_client_window = add_widgets.ClientAddWindow()

    def item_widget_setup(self):
        self.item_widget = QtWidgets.QWidget()
        self.item_widget.setObjectName('item_widget')
        self.item_widget.setWindowTitle('Items')

        btn_all_items = QtWidgets.QPushButton('All items')
        btn_all_items.setObjectName('btn_all_items')

    def category_widget_setup(self):
        self.category_widget = QtWidgets.QWidget()
        self.category_widget.setObjectName('category_widget')
        self.category_widget.setWindowTitle('Category')

        self.lnedit_category = QtWidgets.QLineEdit()
        self.lnedit_category.setPlaceholderText('enter category name')

        btn_category_all = QtWidgets.QPushButton('Show all')
        btn_category_all.setObjectName('btn_category_all')
        btn_category_all.clicked.connect(self.btn_category_all_clicked)

        btn_category_find = QtWidgets.QPushButton('Show find')
        btn_category_find.setObjectName('btn_category_find')
        btn_category_find.clicked.connect(self.btn_category_find_clicked)

        btn_category_add = QtWidgets.QPushButton('Add')
        btn_category_add.setObjectName('btn_category_add')
        btn_category_add.clicked.connect(self.act_category_add_clicked)

        layout_1 = QtWidgets.QHBoxLayout()
        layout_1.addWidget(self.lnedit_category)

        layout_2 = QtWidgets.QHBoxLayout()
        layout_2.addWidget(btn_category_all)
        layout_2.addWidget(btn_category_find)
        layout_2.addWidget(btn_category_add)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_1)
        layout_main.addLayout(layout_2)

        self.category_widget.setLayout(layout_main)

        self.add_category_window = add_widgets.CategoryAddWindow()

    # *************************** LOGIC **************************************
    # *************************** EVENTS/ACTIONS **************************************
    def checkbox_status_clicked(self):
        self.action_show_all_rentals()

    def btn_category_all_clicked(self):
        self.action_show_all_category()

    def btn_category_find_clicked(self):
        pass

    def act_category_add_clicked(self):
        self.add_category_window.show()

    def btn_client_all_clicked(self):
        self.action_show_all_clients()

    def btn_client_find_clicked(self):
        pass

    def act_client_add_clicked(self):
        self.add_client_window.show()

    def btn_rental_all_clicked(self):
        self.action_show_all_rentals()

    def btn_rental_find_clicked(self):
        pass

    def act_rental_add_clicked(self):
        self.add_rental_window.show()

    # ***************************** ACTIONS **************************************
    def action_show_all_clients(self):
        clients = db.get_client_all()
        model = self.make_model(clients, HEADERS_CLIENTS, self.make_table_clients, self.lnedit_client)
        self.draw_table(model)

    def action_show_all_rentals(self):
        rentals = db.get_rental_all()
        model = self.make_model(rentals, HEADERS_RENTALS, self.make_table_rentals, self.lnedit_rental)
        self.draw_table(model)

    def action_show_all_category(self):
        cats = db.get_category_all()
        model = self.make_model(cats, HEADERS_CATS, self.make_table_category, self.lnedit_category)
        self.draw_table(model)


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
        filter_proxy_model.setFilterKeyColumn(model.columnCount()-1)

        lnedit.textChanged.connect(filter_proxy_model.setFilterRegExp)
        return filter_proxy_model

    # @staticmethod
    def make_table_rentals(self, rentals:list):
        if self.checkbox_status.isChecked():
            table = [[rent, rent.Client, rent.rental_date, rent.details, rent.rental_status, rent.rental_name] for rent in rentals]
        else:
            table = [[rent, rent.Client, rent.rental_date, rent.details, rent.rental_status, rent.rental_name] for rent
                     in rentals if rent.rental_status]
        return table

    def make_table_category(self, cats:list):
        table = [[cat, cat.category_name] for cat in cats]
        return table

    @staticmethod
    def make_table_clients(clients:list):
        table = [[client, client.phone_number, client.email, client.client_name] for client in clients]
        return table

    def draw_table(self, model):
        self.table_widget.setModel(model)

        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_widget.setItemDelegate(BaseDelegate())
        self.table_widget.selectionModel().currentChanged.connect(lambda x: print(type(x.data())))
        self.table_widget.hideColumn(model.columnCount()-1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(style)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
