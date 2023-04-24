from typing import Any, Union
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QModelIndex
from binary_dump import read_from_binary, write_into_binary

import dbConnector as db
from alchemy_models import RentalDB, ItemDB
from constants import *


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

    def get_active_orm_object(self):
        """ Возвращает ОРМ обьект активной клетки """
        row = self.get_active_cell_index().row()
        model = self.get_active_model()
        col = model.columnCount() - 1
        orm_obj = model.data(model.index(row, col))
        return orm_obj

    def get_orm_object_from_row(self, row):
        model = self.get_active_model()
        col = model.columnCount() - 1
        orm_obj = model.data(model.index(row, col))
        return orm_obj

    def undo_change(self):
        """ Отменяет последнее изменение в модели """
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

    def save_changes(self):
        changes_list: dict = self._get_unique_changes()
        for index, value in changes_list.items():
            col = index.column()
            orm_obj = self.get_orm_object_from_row(index.row())
            saving_field = ORM_OBJ_COL_NAMES.get(self.parent.get_db_table_name())[col]

            setattr(orm_obj, saving_field, value)
        db.session.commit()

    def reset_changed_cells(self):
        self.changed_cells.clear()


class SearchCacheCategories:
    def __init__(self):
        self.cats_items: dict = {}  # список предметов в категории

    def load_categories(self):
        cats_list = db_cache['category']
        if cats_list:
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

        for loader in self.data_loaders.values():
            loader.loading_thread.data_loaded.connect(self.update_from_Thread)

    def load_all_from_db(self):
        """ Загружает все таблицы из базы данных """
        for name in self.db_tables_objs.keys():
            # self.cache_dict[name] = self.data_loaders.get(name).load_all()
            self.data_loaders.get(name).load_all()

    def refresh_table_cache(self, table_name):
        """ Обновляет кеш для конкретной таблицы заново загружая его из БД"""
        if table_name not in self.db_tables_objs.keys():
            raise ValueError('Wrong table name')
        self.data_loaders[table_name].load_all()
        print('DB Connection Used')

    def update_from_Thread(self, data:list, name:str):
        """ Через эту функцию поток должен закидывать в кеш_дикт загруженные значения"""
        self.cache_dict[name] = data
        print('updated')

    def load_from_offline(self):
        """ Загружает из файла последнее состояние базы данных по приложению """
        offline_cache = read_from_binary(binary_file_name)
        if offline_cache:
            self.cache_dict = offline_cache
            print('Loaded from binary')

    def save_to_binary_file(self):
        """ Сохраняет в файл состояние кеша перед выходом """
        write_into_binary(binary_file_name, self.cache_dict)
        print('Saved to binary')

    def __repr__(self):
        pass

    def __getitem__(self, item):
        return self.cache_dict.get(item, False)


# общий для всех обьект кеша БД на который все классы могу ссылаться



db_cache = DbCache()
db_cache.load_from_offline() # загружает оффлайн файл последнего состояния БД

if __name__ == '__main__':
    # db_cache.load_all_from_db()
    # print(db_cache[''])
    pass
