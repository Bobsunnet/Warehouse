from sqlalchemy import Column, Integer, ForeignKey, String, Date, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from engine_session import get_engine

engine = get_engine(echo=True)
Base = declarative_base()


class ItemDB(Base):
    __tablename__ = 'item'

    item_id = Column(Integer, primary_key=True)
    item_name = Column(String(150), nullable=False)
    category_id = Column(Integer, ForeignKey('category.category_id'))
    amount = Column(Integer)

    Category = relationship("CategoryDB", back_populates='Item')
    # rentals = relationship("RentalDB", back_populates='items')

    def __repr__(self):
        return f'Item: {self.item_name}'

    def __str__(self):
        return f"[ORM] {self.item_name}"

    @staticmethod
    def get_name_parameter():
        return 'item'


class CategoryDB(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(150), nullable=False)

    Item = relationship('ItemDB', back_populates='Category')

    def __repr__(self):
        return f'Category: {self.category_name}'

    def __str__(self):
        return f"[ORM] {self.category_name}"

    @staticmethod
    def get_name_parameter():
        return 'category'


class ClientDB(Base):
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True)
    client_name = Column(String(150), nullable=False)
    phone_number = Column(String(30))
    email = Column(String(100))

    Rental = relationship("RentalDB", back_populates='Client')

    def __repr__(self):
        return f'Client: {self.client_name}'

    def __str__(self):
        return f"[ORM] {self.client_name}"

    @staticmethod
    def get_name_parameter():
        return 'client'


class RentalDB(Base):
    __tablename__ = 'rental'

    rental_id = Column(Integer, primary_key=True)
    rental_name = Column(String(150), nullable=False)
    rental_date = Column(Date)
    client_id = Column(Integer, ForeignKey('client.client_id'))
    details = Column(Text)
    rental_status = Column(Boolean)

    Client = relationship("ClientDB", back_populates='Rental')
    items = relationship("ItemOnRentDB", back_populates='Rental')

    def __repr__(self):
        return f'Rental {self.rental_name}'

    def __str__(self):
        return f"[ORM] {self.rental_name}"

    @staticmethod
    def get_name_parameter():
        return 'rental'


class ItemOnRentDB(Base):
    __tablename__ = 'items_on_rent'

    item_rent_id = Column(Integer, primary_key=True)
    rental_id = Column(Integer, ForeignKey('rental.rental_id'))
    item_id = Column(Integer, ForeignKey('item.item_id'))
    amount = Column(Integer)

    Rental = relationship("RentalDB")
    Item = relationship("ItemDB")

    def __repr__(self):
        return f'Item_on_rent Object'


class LostOnRentDB(Base):
    __tablename__ = 'lost_on_rent'

    lost_item_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.item_id'))
    rental_id = Column(Integer, ForeignKey('rental.rental_id'))
    amount = Column(Integer)
    missing_status = Column(Boolean)

    Rental = relationship("RentalDB")
    Item = relationship("ItemDB")

    def __repr__(self):
        return f'Lost_on_rent Object'


if __name__ == '__main__':
    pass
