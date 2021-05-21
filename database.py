from contextlib import contextmanager
from typing import List

from sqlalchemy.sql import func

from base import Base, engine, Session
from fee import Fee


class DataBase:
    def __init__(self):
        Base.metadata.create_all(engine)

    @contextmanager
    def __session_reading(self):
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
    def __session_writing(self):
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

    def add_fee(self, fee: Fee):
        session = Session()
        session.add(fee)
        session.commit()
        session.close()

    def get_fee(self, id: int) -> Fee:
        session = Session()
        result = (session.query(Fee)
                    .filter(Fee.id == id)
                    .first())
        session.close()
        return result

    def get_fees(self) -> List[Fee]:
        session = Session()
        result = session.query(Fee).all()
        session.close()
        return result

    def update_fee_check(self, id: int, check: bool):
        session = Session()
        (session.query(Fee)
            .filter(Fee.id == id)
            .update({Fee.check: check}))
        session.commit()
        session.close()

    def saved_money(self) -> int:
        session = Session()
        result = (session.query(func.sum(Fee.value))
                        .filter(Fee.check)
                        .one()[0])
        session.close()
        return result if result else 0

    def missing_money(self) -> int:
        session = Session()
        result = (session.query(func.sum(Fee.value))
                        .filter(Fee.check == False)
                        .one()[0])
        session.close()
        return result if result else 0

    def fees_checked(self) -> int:
        session = Session()
        result = (session.query(Fee)
                        .filter(Fee.check)
                        .count())
        session.close()
        return result

    def fees_not_checked(self) -> int:
        session = Session()
        result = (session.query(Fee)
                        .filter(Fee.check == False)
                        .count())
        session.close()
        return result
