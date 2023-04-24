import sys
import os
import psycopg2.errors as psyc_ex

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, QSortFilterProxyModel, Qt
from PyQt5.QtGui import QIcon, QKeySequence


from alchemy_models import RentalDB
from TableInterface import TableModel, BaseDelegate, MyTableView
import dbConnector as db
import add_widgets
from find_widgets import FindWidget
from OperationClasses import SearchCacheCategories, db_cache, ModelCache

from constants import *


BASEDIR = os.path.dirname(__file__)
STYLES_PATH = os.path.join(BASEDIR, 'static/style/styles.css')

with open(STYLES_PATH, 'r') as file:
    style = file.read()


class DetailedRentalWidget(QWidget, SearchCacheCategories):
    # виджет для просмотра подробных сведений об объекте(Rental)
    def __init__(self, parent):
        super().__init__()
        self.table_model = None
        self.parent: QtWidgets.QWidget = parent
        self.rental_object: RentalDB | None = None
        self.model_cache = ModelCache
        self.ui_is_setuped = False

        self.init_ui()

        self.table_widget.horizontalHeader().sectionDoubleClicked.connect(self.parent.sorting_double_clicked)


    def init_ui(self):
        self.setMinimumSize(600,480)

        self.table_widget = MyTableView()
        self.lbl_rent_name = QLabel()
        self.cbox_category = QComboBox(self)
        self.cbox_item = QComboBox(self)
        self.btn_add = QPushButton(self)
        self.btn_reset = QPushButton(self)
        self.btn_save = QPushButton(self)

        self.layouts = {}
        self.layouts['main'] = QVBoxLayout()
        self.setLayout(self.layouts['main'])
        self.layouts['main'].insertSpacing(0, 20)

        self.layouts['info_top'] = QHBoxLayout()
        self.layouts['info_top'].addWidget(self.lbl_rent_name)
        self.layouts['info_top'].addSpacing(200)
        self.layouts['info_top'].addWidget(self.btn_reset)
        self.layouts['info_top'].addWidget(self.btn_save)

        self.layouts['search_top'] = QHBoxLayout()
        self.layouts['search_top'].addWidget(self.cbox_category, 4)
        self.layouts['search_top'].addWidget(self.cbox_item, 4)
        self.layouts['search_top'].addWidget(self.btn_add, 2)

        self.layouts['main'].addLayout(self.layouts['info_top'])
        self.layouts['main'].addLayout(self.layouts['search_top'])
        self.layouts['main'].addWidget(self.table_widget)

    def setup_ui(self):
        self.load_categories()

        self.btn_reset.setText('Reset Editing')
        self.btn_reset.setObjectName('btn_reset')

        self.btn_add.setText('+')
        self.btn_save.setText('Save Editing')

        self.cbox_category.addItems(list(self.cats_items.keys()))
        self.cbox_item.addItems(self.cats_items.get(self.cbox_category.currentText(), ['None']))
        self.cbox_category.currentTextChanged.connect(self._change_search_box_items)
        self.ui_is_setuped = True

    def setModel(self, model):
        # сохраняем текущую модель для таблицы
        self.table_model = model
        self._activate_table_model()

    def _activate_table_model(self):
        self.table_widget.setModel(self.table_model)

    def set_rental(self, rental: RentalDB):
        """ Подключает событие rental к виджету, далее вызывает метод создание модели """
        self.rental_object = rental
        self.setModel(self._create_items_model(rental))
        self.lbl_rent_name.setText(f"__EVENT__: {rental.rental_name}, __DATE__:{rental.rental_date}")

    def _change_search_box_items(self, category_name:str):
        self.cbox_item.clear()
        self.cbox_item.addItems(self.cats_items[category_name])

    @staticmethod
    def _create_items_model(rental):
        """ Создание модели для таблицы из обьекта ОРМ """
        items_list = rental.items
        items_table = [(item.Item.item_name, item.amount) for item in items_list] # делаем таблицу: (название, к-тво)
        model = TableModel(items_table, ['Name', 'Amount'])
        return model


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_cache = db_cache # уже созданный общий кеш
        self.db_cache.load_all_from_db()
        self.active_widget = None

        self.actions_menu_setup()
        self.warehouse_widget_setup()
        self.rental_widget_setup()
        self.client_widget_setup()
        self.item_widget_setup()
        self.category_widget_setup()
        self.mainWindow_setup()
        self.layout_setup()

    def actions_menu_setup(self):
        """ Подключение менюбара и действий(QAction) """
        self.action_undo_changes = QtWidgets.QAction('Undo', self)  #
        self.action_undo_changes.triggered.connect(self.undo_changes)
        self.action_undo_changes.setShortcut(QKeySequence('Ctrl+Z'))

        self.action_save_changes = QtWidgets.QAction('Save', self)  #
        self.action_save_changes.triggered.connect(self.save_changes)
        self.action_save_changes.setShortcut(QKeySequence('Ctrl+S'))

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.file_menu.addAction(self.action_undo_changes)
        self.file_menu.addAction(self.action_save_changes)

    def mainWindow_setup(self):
        self.setGeometry(200, 150, 800, 700)
        self.setMinimumSize(800,700)
        toolbar = QtWidgets.QToolBar('Main toolbar')
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # это один виджет в окне. просто меняем модели для него в процессе
        self.table_view_main = MyTableView()
        self.table_view_main.setObjectName('table_widget')
        self.table_view_main.horizontalHeader().sectionDoubleClicked.connect(self.sorting_double_clicked)

        # виджет для просмотра подробностей о работе или обьекте. Открывается в отдельном окне
        self.detailed_window = DetailedRentalWidget(self)

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

        self.widgets_list = [self.warehouse_widget, self.rental_widget, self.client_widget, self.item_widget,
                        self.category_widget]

        for w in self.widgets_list:
            self.tab_window.addTab(w, w.windowTitle())

    def layout_setup(self):
        main_layout = QtWidgets.QVBoxLayout()

        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.tab_window)
        splitter.addWidget(self.table_view_main)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([125, 150])
        main_layout.addWidget(splitter)

        main_block_widget = QWidget()
        main_block_widget.setObjectName('main_block_widget')

        main_block_widget.setLayout(main_layout)

        self.setCentralWidget(main_block_widget)

    def warehouse_widget_setup(self):
        self.warehouse_widget = QWidget()
        self.warehouse_widget.setObjectName('warehouse_widget')
        self.warehouse_widget.setWindowTitle('Warehouse')

    def rental_widget_setup(self):
        self.rental_widget = FindWidget('rental_widget', 'rental', HEADERS_RENTALS)

        self.rental_widget.checkbox_status = QtWidgets.QCheckBox('Show Ended')
        self.rental_widget.layout_1.addWidget(self.rental_widget.checkbox_status)

        self.rental_widget.checkbox_status.clicked.connect(self.checkbox_status_clicked)
        self.rental_widget.btn_add_object.clicked.connect(self.act_rental_add_clicked)
        self.rental_widget.btn_edit_object.clicked.connect(self.btn_edit_rental_clicked)
        self.rental_widget.btn_delete_row.clicked.connect(self.btn_delete_row_clicked)
        self.rental_widget.btn_show_full_table.clicked.connect(self.btn_show_full_rental_clicked)
        self.rental_widget.btn_save_changes.clicked.connect(self.action_save_changes.trigger)

        self.add_rental_window = add_widgets.RentalAddWindow(self, 'add_rental_window','Rental')

    def client_widget_setup(self):
        self.client_widget = FindWidget('client_widget', 'client', HEADERS_CLIENTS)

        self.client_widget.btn_add_object.clicked.connect(self.act_client_add_clicked)
        self.client_widget.btn_edit_object.clicked.connect(self.btn_edit_client_clicked)
        self.client_widget.btn_show_full_table.clicked.connect(self.btn_show_full_clients_clicked)
        self.client_widget.btn_save_changes.clicked.connect(self.action_save_changes.trigger)

        self.add_client_window = add_widgets.ClientAddWindow(self, 'add_client_window', 'Client')

    def item_widget_setup(self):
        self.item_widget = FindWidget('item_widget', 'item', HEADERS_ITEMS)

        self.item_widget.btn_add_object.clicked.connect(self.act_item_add_clicked)
        self.item_widget.btn_edit_object.clicked.connect(self.btn_edit_items_clicked)
        self.item_widget.btn_show_full_table.clicked.connect(self.btn_show_full_items_clicked)
        self.item_widget.btn_save_changes.clicked.connect(self.action_save_changes.trigger)

        self.add_item_window = add_widgets.ItemAddWindow(self,'add_item_window','Item')

    def category_widget_setup(self):
        self.category_widget = FindWidget('category_widget', 'category', HEADERS_CATS)

        self.category_widget.btn_add_object.clicked.connect(self.act_category_add_clicked)
        self.category_widget.btn_edit_object.clicked.connect(self.btn_edit_category_clicked)
        self.category_widget.btn_show_full_table.clicked.connect(self.btn_show_full_category_clicked)
        self.category_widget.btn_save_changes.clicked.connect(self.action_save_changes.trigger)

        self.add_category_window = add_widgets.CategoryAddWindow(self,'add_category_window','Category')

    def closeEvent(self, event) -> None:
        print('Saving dump binary file')
        self.db_cache.save_to_binary_file()
        event.accept()

# ************************************************* LOGIC *********************************************************
    def debug_versatile(self):
        print('Debug is not connected now')

    def sorting_double_clicked(self, col):
        # todo переделать так чтобы метод сорт вызывался из класса MyTableView
        model = self.table_view_main.model()
        if self.table_view_main.asc_sorting_order():
            model.sort(col, Qt.AscendingOrder)
            self.table_view_main.change_sorting_order()
        else:
            model.sort(col, Qt.DescendingOrder)
            self.table_view_main.change_sorting_order()

    def undo_changes(self):
        widget = self.tab_window.currentWidget()
        if isinstance(widget, FindWidget):
            self.tab_window.currentWidget().model_cache.undo_change()

    def save_changes(self):
        widget = self.tab_window.currentWidget()
        if isinstance(widget, FindWidget):
            self.tab_window.currentWidget().model_cache.save_changes()

    def get_db_table_name(self) -> str:
        """ Возвращает имя связанной таблицы для текущего виджета"""
        return self.tab_window.currentWidget().get_db_table_name()

    # *************************** EVENTS/ACTIONS **************************************
    def tab_changed(self, i):
        if i == 1:
            self.action_show_full_table(self.make_table_rentals)
        elif i == 2:
            self.action_show_full_table(self.make_table_clients)
        elif i == 3:
            self.action_show_full_table(self.make_table_items)
        elif i == 4:
            self.action_show_full_table(self.make_table_category)

    def checkbox_status_clicked(self):
        self.action_show_full_table(self.make_table_rentals)

    # 1
    def btn_show_full_category_clicked(self):
        # здесь и далее скидываем кеш, чтобы загрузить измененную таблицу из БД
        self.refresh_cache(self.get_db_table_name())
        self.action_show_full_table(self.make_table_category)
        self.category_widget.model_cache.reset_changed_cells() # сбрасывает стек несохраненных изменений таблицы

    def btn_edit_category_clicked(self):
        res = self.category_widget.model_cache.get_active_cell_data()
        print(type(res), res)

    def act_category_add_clicked(self):
        self.add_category_window.show()

    # 2
    def btn_show_full_clients_clicked(self):
        self.refresh_cache(self.get_db_table_name())
        self.action_show_full_table(self.make_table_clients)
        self.client_widget.model_cache.reset_changed_cells()

    def btn_edit_client_clicked(self):
        print(f'editing: {self.client_widget.model_cache.get_active_cell_data()}')

    def act_client_add_clicked(self):
        self.add_client_window.show()

    # 3
    def btn_show_full_rental_clicked(self):
        self.refresh_cache(self.get_db_table_name())
        self.action_show_full_table(self.make_table_rentals)
        self.rental_widget.model_cache.reset_changed_cells()

    def btn_edit_rental_clicked(self):
        self.detailed_window.close() # закрываем окно если открыто

        rental = self.rental_widget.model_cache.get_active_orm_object() # в переменной должен быть обьект из ОРМ
        if isinstance(rental, RentalDB):
            self.detailed_window.set_rental(rental) # здесь автоматически строится модель
            if not self.detailed_window.ui_is_setuped:
                self.detailed_window.setup_ui()
            self.detailed_window.show()
        else:
            self.draw_caution_window('Спочатку оберіть подію', "Необрано подію")

    def btn_delete_row_clicked(self):
        rental = self.rental_widget.model_cache.get_active_orm_object()
        deletion_res = self.delete_rental(rental)


    def delete_rental(self, rental) -> bool | None:
        """ Возвращает True если удаление выполнилось иначе None"""
        if isinstance(rental, RentalDB):
            try:
                db.session.delete(rental)
                db.session.commit()
                self.refresh_cache('rental')
                self.action_show_full_table(self.make_table_rentals)
                return True

            except psyc_ex.IntegrityError as FK_violation_ex:
                db.session.rollback()
                self.draw_error_window('Загальна помилка видалення', 'Помилка видалення', FK_violation_ex)

            except Exception as ex:
                db.session.rollback()
                self.draw_error_window('Загальна помилка видалення', 'Помилка видалення', ex)

        else:
            self.draw_caution_window('Видаляти можна тільки рядок', 'Помилка видалення')


    def act_rental_add_clicked(self):
        self.add_rental_window.cbox_setup()
        self.add_rental_window.show()

    # 4
    def btn_show_full_items_clicked(self):
        self.refresh_cache(self.get_db_table_name())
        self.action_show_full_table(self.make_table_items)
        self.item_widget.model_cache.reset_changed_cells()

    def btn_edit_items_clicked(self):
        print(self.item_widget.model_cache.get_active_cell_data())

    def act_item_add_clicked(self):
        self.add_item_window.cbox_setup()
        self.add_item_window.show()

    # ***************************** ACTIONS **************************************
    def action_show_full_table(self, table_convert_func):
        """ Метод рисует таблицу на основе кеша без загрузки из ДБ"""
        widget: FindWidget = self.tab_window.currentWidget()
        orm_obj_list = self.db_cache.cache_dict[widget.db_table_name]
        model = self.make_model(orm_obj_list, widget.headers, table_convert_func,
                                widget.lnedit_search)
        widget.model_cache.set_active_model(model)

        self.table_setup(widget.model_cache.get_active_model(), widget)

    def refresh_cache(self, table_name:str):
        """ загружает из БД данные для нужной таблицы в кеш """
        self.db_cache.refresh_table_cache(table_name)

    def refresh_cache_all(self):
        """ обновляет все данные кеша БД """
        self.db_cache.load_all_from_db()

    # *************************** FUNCTIONS **************************************
    def draw_caution_window(self, message, error_type, exception=None):
        caution_window = QtWidgets.QMessageBox()
        caution_window.setWindowTitle(error_type)
        caution_window.setText(message)
        caution_window.setInformativeText(f'Exception text: {exception}')

        caution_window.exec_()

    def draw_error_window(self, message, error_type, exception):
        caution_window = QtWidgets.QMessageBox()
        caution_window.setWindowTitle(error_type)
        caution_window.setText(message)
        caution_window.setInformativeText(f'Exception text: {exception}')

        caution_window.exec_()

    @staticmethod
    def make_model(obj_lst, headers, table_func, lnedit):
        """Make a model for proper table

        :param obj_lst: List of ORM objects
        :param headers: Header for model
        :param table_func: Func-converter for table
        :param lnedit: LineEdit connected to type of table
        :return: model with connected filter """

        table = table_func(obj_lst)
        model = TableModel(table, headers)
        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(0)

        lnedit.textChanged.connect(filter_proxy_model.setFilterRegExp)
        return filter_proxy_model

    def make_table_rentals(self, rentals: list):
        if self.rental_widget.checkbox_status.isChecked():
            table = [[rent.rental_name, rent.Client, rent.rental_date, rent.details, rent.rental_status,
                      rent] for rent in rentals]
        else:
            table = [[rent.rental_name, rent.Client, rent.rental_date, rent.details, rent.rental_status,
                      rent] for rent in rentals if rent.rental_status]
        return table

    @staticmethod
    def make_table_items(items: list):
        table = [[item.item_name, item.Category, item.amount, item] for item in items]
        return table

    @staticmethod
    def make_table_category(cats: list):
        table = [[cat.category_name, cat] for cat in cats]
        return table

    @staticmethod
    def make_table_clients(clients: list):
        table = [[client.client_name, client.phone_number, client.email, client] for client in clients]
        return table

    def table_setup(self, model, widget):
        self.table_view_main.setModel(model)
        self.table_view_main.setItemDelegate(BaseDelegate())
        self.table_view_main.selectionModel().currentChanged.connect(lambda x: widget.model_cache.set_active_cell_data(x.data()))
        self.table_view_main.selectionModel().currentChanged.connect(self.tab_window.currentWidget().model_cache.set_active_cell_index)
        self.table_view_main.selectionModel().currentChanged.connect(self.cell_highlighted)

        # self.table_widget.selectionModel().currentChanged.connect(self.tab_window.currentWidget().add_changed_cell)

        self.table_view_main.horizontalHeader().setSectionResizeMode(3)
        # self.table_widget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        filtered_column = model.columnCount()-1
        self.table_view_main.setFilterColumn(filtered_column) # прячет колонку в таблице по которой фильтруется содержимое

    def cell_highlighted(self, current: QtCore.QModelIndex, previous:QtCore.QModelIndex):
        if previous.column() != -1:
            widget = self.tab_window.currentWidget()
            model = self.table_view_main.model()
            widget.model_cache.add_changed_cell(model.itemData(previous).get(0))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(style)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
