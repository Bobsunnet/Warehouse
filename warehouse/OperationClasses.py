from typing import Any, Union
from PyQt5.QtWidgets import QTableView, QWidget
from PyQt5.QtCore import QModelIndex

import dbConnector as db


class ModelCache:
    """ Хранит данные о текущей модели и ее изменениях """

    def __init__(self, parent: QWidget = None):
        self._active_cell_data: Any = None  # запоминает выбранную клетку в таблице и текущую модель, которая хранится в кеше
        self._previous_cell_data: Any = None
        self._previous_cell_index: QModelIndex | None = None
        self._active_cell_index: QModelIndex | None = None
        self._active_model = None
        self.changed_cells: list = []  # стек изменений значений таблицы
        self.parent = parent

    def add_changed_cell(self, changed_data: Any):
        if changed_data != self._previous_cell_data:
            self.changed_cells.append((self._previous_cell_index, self._previous_cell_data, changed_data))
            print(self.changed_cells)

    def _set_previous_cell_data(self):
        if self._active_cell_data is not None:
            self._previous_cell_data = self._active_cell_data

    def _set_previous_cell_index(self):
        if self._active_cell_index is not None:
            self._previous_cell_index = self._active_cell_index

    def set_active_cell_data(self, value):
        self._set_previous_cell_data()
        self._active_cell_data = value

    def get_active_cell_data(self):
        return self._active_cell_data

    def set_active_model(self, model):
        self._active_model = model

    def get_active_model(self):
        return self._active_model

    def set_active_cell_index(self, index):
        self._set_previous_cell_index()
        self._active_cell_index = index

    def get_active_cell_index(self):
        return self._active_cell_index

    def undo_change(self):
        if len(self.changed_cells) > 0:
            last_change = self.changed_cells.pop()
            index, old_value = last_change[0:2]
            self._active_model.setData(index, old_value)

    def _get_unique_changes(self):
        """ проходит по списку изменений и оставляет от каждого индекса только последний вариант """
        unique_changes = {}
        for changes in self.changed_cells[::-1]:
            unique_changes.setdefault(changes[0], changes[2])
        return unique_changes


class SearchCacheCategories:  # todo сделать без этого класса. Через общий DbCache class
    def __init__(self):
        self.cats_items: dict = {}  # список предметов в категории

    def load_categories(self):
        cats_list = db.DataLoader(db.CategoryDB).load_all()
        for el in cats_list:
            self.cats_items[el.category_name] = [item.item_name for item in el.Item]


class DbCache:
    """ Хранит загружаемые данные из БД чтоб минимизировать обращения к БД """

    def __init__(self):
        """ cache_dict: - словарь со списками обьектов ОРМ"""
        self.cache_dict: dict = {}
        self.db_tables_objs: dict = {'item': db.ItemDB,
                                     'rental': db.RentalDB,
                                     'client': db.ClientDB,
                                     'category': db.CategoryDB}

        self.data_loaders: dict = {'item': db.DataLoader(db.ItemDB),
                                   'rental': db.DataLoader(db.RentalDB),
                                   'client': db.DataLoader(db.ClientDB),
                                   'category': db.DataLoader(db.CategoryDB)}

    def load_all_from_db(self):
        """ Загружает все таблицы из базы данных """
        for name in self.db_tables_objs.keys():
            self.cache_dict[name] = self.data_loaders.get(name).load_all()
            print('DB Connection Used')

    def refresh_table_cache(self, table_name):
        """ Обновляет кеш для конкретной таблицы заново загружая его из БД"""
        if table_name not in self.db_tables_objs.keys():
            raise ValueError('Wrong table name')
        self.cache_dict[table_name] = self.data_loaders[table_name].load_all()
        print('DB Connection Used')


if __name__ == '__main__':
    s = SearchCacheCategories()
    s.load_categories()
