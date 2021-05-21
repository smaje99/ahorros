from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///ahorros.db')

Session = sessionmaker(bind=engine)

Base = declarative_base()


@contextmanager
def session_reading():
    '''Proporciona un alcance transaccional en
    torno a una serie de operaciones para lectura

    Yields:
        Session: serie de operaciones para lectura
    '''
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()

@contextmanager
def session_writing():
    '''Proporciona un alcance transaccional en
    torno a una serie de operaciones para escritura

    Yields:
        Session: serie de operaciones para escritura
    '''
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
