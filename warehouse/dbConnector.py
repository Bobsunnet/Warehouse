from datetime import date

from PyQt5.QtCore import QDate

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
def get_item_model(item: int | str):
    if type(item) == str:
        return session.query(ItemDB).filter(ItemDB.item_name == item).first()
    elif type(item) == int:
        return session.query(ItemDB).filter(ItemDB.item_id == item).first()
    else:
        return


@data_getter_deco
def get_rental_model(rental: int | str):
    if type(rental) == str:
        return session.query(RentalDB).filter(RentalDB.rental_name == rental).first()
    elif type(rental) == int:
        return session.query(RentalDB).filter(RentalDB.rental_id == rental).first()
    else:
        return


@data_getter_deco
def get_rental_all():
    return session.query(RentalDB).all()


@data_getter_deco
def get_client_model(client: int | str):
    '''

    :param client: ID: int or Name: str
    :return: ORM object
    '''
    if type(client) == str:
        return session.query(ClientDB).filter(ClientDB.client_name == client).first()
    elif type(client) == int:
        return session.query(ClientDB).filter(ClientDB.client_id == client).first()
    else:
        return


@data_getter_deco
def get_client_all() -> list:
    return session.query(ClientDB).all()


@data_getter_deco
def get_category_model(category: int | str):
    if type(category) == str:
        return session.query(CategoryDB).filter(CategoryDB.category_name == category).first()
    elif type(category) == int:
        return session.query(CategoryDB).filter(CategoryDB.category_id == category).first()
    else:
        return


@data_getter_deco
def get_category_all() -> list:
    return session.query(CategoryDB).all()


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
def convert_to_table(obj_list: list):
    resulting_table = []
    for el in obj_list:
        resulting_table.append(tuple(el.__dict__.items())[1:])
    return resulting_table


def get_full_table(table_object: Base, tupled=False):
    items = session.query(table_object).all()
    if not tupled:
        return items
    return convert_to_table(items)


if __name__ == '__main__':
    # rentals = get_rental_all()
    # table = [[rent, rent.Client, rent.rental_date, rent.details, rent.rental_status] for rent in rentals]
    add_rental('test')
    pass
