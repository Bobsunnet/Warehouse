import sys
from datetime import date

from engine_session import *
from alchemy_models import *

Session = get_session()
session = Session()


def commit_addition(res):
    try:
        session.commit()
        return f'[SUCCESS]: {res}'
    except Exception as ex:
        session.rollback()
        print(f'[ERROR]: {ex}')


def data_getter_deco(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except Exception as ex:
            print(f'[ERROR]: {ex}')
            return

    return wrapper


@data_getter_deco
def get_obj_single(obj: Base, parameter: int | str):
    '''

    :param parameter: ID: int or Name: str
    :return: ORM object
    '''
    name_parameter = obj.get_name_parameter()
    if type(parameter) == str:
        return session.query(obj).filter(getattr(obj, f'{name_parameter}_name') == parameter).first()
    elif type(parameter) == int:
        return session.query(obj).filter(getattr(obj, f'{name_parameter}_id') == parameter).first()
    else:
        return


@data_getter_deco
def get_category_model(category: int | str):
    if type(category) == str:
        return session.query(CategoryDB).filter(CategoryDB.category_name == category).first()
    elif type(category) == int:
        return session.query(CategoryDB).filter(CategoryDB.category_id == category).first()
    else:
        return


@data_getter_deco
def get_object_all(obj: Base):
    return session.query(obj).all()


def add_category(cat_name):
    category_add = CategoryDB(category_name=cat_name)
    res = session.add(category_add)
    commit_addition(res)


def add_item(item_name, cat_id, amount=0):
    item_add = ItemDB(item_name=item_name, amount=amount, category_id=cat_id)
    res = session.add(item_add)
    commit_addition(res)


def add_client(name, phone='', email=''):
    client_add = ClientDB(client_name=name, phone_number=phone, email=email)
    res = session.add(client_add)
    commit_addition(res)


def add_rental(name, client_id=None, details='', rent_date='', rent_status=True):
    if not rent_date:
        rent_date = date.today()
    rental_add = RentalDB(rental_name=name, client_id=client_id, details=details, rental_date=rent_date,
                          rental_status=rent_status)
    res = session.add(rental_add)
    commit_addition(res)


def add_items_on_rent(item_id, rental_id, amount):
    item_add = ItemOnRentDB(item_id=item_id, rental_id=rental_id, amount=amount)
    res = session.add(item_add)
    commit_addition(res)


def add_items_lost(item_id, rental_id, amount, status=True):
    item_lost = LostOnRentDB(item_id=item_id, rental_id=rental_id, amount=amount, missing_status=status)
    res = session.add(item_lost)
    commit_addition(res)


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


class DataLoader:
    '''
    Class for load interaction with DB through the SQLalchemy classes
    '''
    def __init__(self, orm_class: Base):
        self.orm_class = orm_class

    def load_single(self, name: int | str):
        return get_obj_single(self.orm_class, name)

    def load_all(self):
        return get_object_all(self.orm_class)

    def load_names(self):
        parameter = self.orm_class.get_name_parameter()

        return [getattr(obj, f'{parameter}_name') for obj in self.load_all()]

    def __repr__(self):
        return f'DataLoader for: {self.orm_class}'


if __name__ == '__main__':
    data_l = DataLoader(ItemDB)
    res = data_l.load_all()
    print(sys.getsizeof(res))
    pass
