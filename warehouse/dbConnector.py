import sys
from datetime import date

from PyQt5.QtCore import QThread, pyqtSignal

from engine_session import *
from alchemy_models import *
from exceptionWarehouse import InvalidInputException

Session = get_session()
session = Session()


def try_commit_addition(res):
    try:
        session.commit()
        return f'[SUCCESS]: {res}'
    except Exception as ex:
        session.rollback()
        print(f'[ERROR]: {ex}')


def try_get_data_deco(func):
    def wrapper(*args, **kwargs):
        try:
            loaded_data = func(*args, **kwargs)
            return loaded_data
        except Exception as ex:
            print(f'[ERROR]: {ex}')
            return

    return wrapper


@try_get_data_deco
def get_obj_single(obj: Base, parameter: int | str):
    #TODO Сделать через перегрузку функций или матч кейз
    '''

    :param parameter: obj ID(int) or obj Name(str)
    :return: ORM object
    '''
    name_parameter = obj.get_name_parameter()
    if type(parameter) == str:
        return session.query(obj).filter_combobox(getattr(obj, f'{name_parameter}_name') == parameter).first()
    elif type(parameter) == int:
        return session.query(obj).filter_combobox(getattr(obj, f'{name_parameter}_id') == parameter).first()
    else:
        return


@try_get_data_deco
def get_category_model(category: int | str):
    if type(category) == str:
        return session.query(CategoryDB).filter_combobox(CategoryDB.category_name == category).first()
    elif type(category) == int:
        return session.query(CategoryDB).filter_combobox(CategoryDB.category_id == category).first()
    else:
        return


@try_get_data_deco
def get_object_all(obj: Base):
    return session.query(obj).all()


def create_category(cat_name:str):
    category_add = CategoryDB(category_name=cat_name)
    res = session.add(category_add)
    try_commit_addition(res)


def create_item(item_name, cat_id, amount=0):
    item_add = ItemDB(item_name=item_name, amount=amount, category_id=cat_id)
    res = session.add(item_add)
    try_commit_addition(res)


def create_client(name, phone='', email=''):
    client_add = ClientDB(client_name=name, phone_number=phone, email=email)
    res = session.add(client_add)
    try_commit_addition(res)


def create_rental(name, client_id=None, details='', rent_date='', rent_status=True):
    if not rent_date:
        rent_date = date.today()
    rental_add = RentalDB(rental_name=name, client_id=client_id, details=details, rental_date=rent_date,
                          rental_status=rent_status)
    res = session.add(rental_add)
    try_commit_addition(res)


def add_items_on_rent(item_id, rental_id, amount):
    item_add = ItemOnRentDB(item_id=item_id, rental_id=rental_id, amount=amount)
    res = session.add(item_add)
    try_commit_addition(res)


def add_items_lost(item_id, rental_id, amount, status=True):
    item_lost = LostOnRentDB(item_id=item_id, rental_id=rental_id, amount=amount, missing_status=status)
    res = session.add(item_lost)
    try_commit_addition(res)


# ********************************* SOME TEST FUNC **************************************
def _convert_to_table(obj_list: list):
    resulting_table = []
    for el in obj_list:
        resulting_table.append(tuple(el.__dict__.items())[1:])
    return resulting_table


def get_full_table(table_object: Base, tupled=False):
    items = session.query(table_object).all()
    if not tupled:
        return items
    return _convert_to_table(items)
# ********************************** --------- ************************************************


class LoadDataThread(QThread):
    """ Загружает данные из БД используя указанную функцию загрузки и отдельный поток"""
    data_loaded = pyqtSignal(list, str)
    downloading_finished = pyqtSignal()

    def __init__(self, orm_class: Base):
        super().__init__()
        self._load_function = None # функция загрузки из БД
        self._orm_class = orm_class

    def change_load_function(self, load_function):
        self._load_function = load_function

    def run(self):
        print('started')
        downloaded_data = self._load_function(self._orm_class)
        self.data_loaded.emit(downloaded_data, self._orm_class.get_name_parameter())
        self.downloading_finished.emit()


class DataLoader:
    """ Class for load interaction with DB through the SQLalchemy classes
        starting different Thread """

    def __init__(self, orm_class: Base):
        self.orm_class = orm_class
        self.db_table_name = self.orm_class.get_name_parameter()  # сохраняем имя таблицы

        self.loading_thread = LoadDataThread(self.orm_class) # обьект QThread
        self.loading_thread.change_load_function(get_object_all) # функция загрузчик, которую будет использовать поток

    def load_single(self, name: int | str):
        """ загружает обьект из БД по имени"""
        return get_obj_single(self.orm_class, name)

    def load_all(self) -> list:
        """ загружает все обьекты из таблицы и возвращает список """
        self.loading_thread.start()
        # return get_object_all(self.orm_class)

    # def load_names(self):
    #     """ возвращает список имен из БД"""
    #     return [getattr(obj, f'{self._db_table_name}_name') for obj in self.load_all()]

    def __repr__(self):
        return f'DataLoader for: {self.orm_class}'


if __name__ == '__main__':
    data_l = DataLoader(ItemDB)
    a = ItemDB()
    print(isinstance(ItemDB, Base))
    # res = get_object_all(ItemDB)
    # print(isinstance(ItemDB, ItemDB))


