


class Item:
    def __init__(self, item_id: int, name: str, category_id: str, amount: int):
        self.item_id = item_id
        self.name = name
        self.category_id = category_id
        self.amount = amount


class Rental:
    def __init__(self, rental_name: str, client_id: int, details: str, rental_date: str, finished: bool = False):
        self.rental_name = rental_name
        self.client_id = client_id
        self.details = details
        self.rental_date = rental_date
        self.finished = finished


class Client:
    def __init__(self, client_id: int, client_name: str, phone_number: str, email: str):
        self.client_id = client_id
        self.client_name = client_name
        self.phone_number = phone_number
        self.email = email


class Category:
    def __init__(self, cat_id: int, cat_name: str):
        self.cat_id = cat_id
        self.cat_name = cat_name


class Step:
    def __init__(self, step_name: str):
        self.step_name = step_name


class WareHouse:
    '''после загрузки из БД показывает какие предметы есть в определенном поле'''

    def __init__(self):
        self.items = []

    def get_current_items(self):
        '''достает из БД соответсвующие классу предметы '''
        pass
