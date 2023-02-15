import engine_session as db_engine
from alchemy_models import *

Session = db_engine.get_session()
session = Session()


def committing_deco(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            session.commit()
            return f'[SUCCESS]: {res}'
        except Exception as ex:
            session.rollback()
            print(f'[ERROR]: {ex}')
            return

    return wrapper


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
def get_rental_model(rental: int |str ):
    if type(rental) == str:
        return session.query(RentalDB).filter(RentalDB.rental_name == rental).first()
    elif type(rental) == int:
        return session.query(RentalDB).filter(RentalDB.rental_id == rental).first()
    else:
        return


@data_getter_deco
def get_client_model(client: int | str):
    if type(client) == str:
        return session.query(ClientDB).filter(ClientDB.client_name == client).first()
    elif type(client) == int:
        return session.query(ClientDB).filter(ClientDB.client_id == client).first()
    else:
        return


@committing_deco
def add_category(cat_name):
    category_add = CategoryDB(category_name=cat_name)
    session.add(category_add)


@committing_deco
def add_item(item_name, cat_id, amount=0):
    item_add = ItemDB(item_name=item_name, amount=amount, category_id=cat_id)
    session.add(item_add)


@committing_deco
def add_client(name, phone='', email=''):
    client_add = ClientDB(client_name=name, phone_number=phone, email=email)
    session.add(client_add)


@committing_deco
def add_rental(name, client_id, details='', rent_date='', rent_status=True):
    rental_add = RentalDB(rental_name=name, client_id=client_id, details=details, rental_date=rent_date,
                          rental_status=rent_status)
    session.add(rental_add)


@committing_deco
def add_items_on_rent(item_id, rental_id, amount):
    item_add = ItemOnRentDB(item_id=item_id, rental_id=rental_id, amount=amount)
    session.add(item_add)


@committing_deco
def add_items_lost(item_id, rental_id, amount, status=True):
    item_lost = LostOnRentDB(item_id=item_id, rental_id=rental_id, amount=amount, missing_status=status)
    session.add(item_lost)


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
    print(get_item_model())
