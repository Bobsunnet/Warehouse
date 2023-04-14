import sqlalchemy
from ORM.config import *
from sqlalchemy.orm import sessionmaker


def get_engine(echo=False):
    '''
    creates SQLalchemy database engine from config.py

    :return: Engine()
    '''
    url = f'postgresql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DATABASE}'
    engine = sqlalchemy.create_engine(url, echo=echo)
    return engine


def get_session(echo=False):
    '''
    creates session for certain engine
    :return: session-onject
    '''
    engine = get_engine(echo)
    session = sessionmaker(bind=engine)
    return session




