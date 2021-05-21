from typing import List

from sqlalchemy.sql import func

from base import Base, engine, session_reading, session_writing
from fee import Fee


class DataBase:
    def __init__(self):
        Base.metadata.create_all(engine)

    def add_fee(self, fee: Fee):
        with session_writing() as session:
            session.add(fee)

    def get_fee(self, id: int) -> Fee:
        with session_reading() as session:
            result = (session.query(Fee)
                        .filter(Fee.id == id)
                        .first())
        return result

    def get_fees(self) -> List[Fee]:
        with session_reading() as session:
            result = session.query(Fee).all()
        return result

    def update_fee_check(self, id: int, check: bool):
        with session_writing() as session:
            (session.query(Fee)
                .filter(Fee.id == id)
                .update({Fee.check: check}))

    def money(self, saved: bool) -> int:
        with session_reading() as session:
            result = (session.query(func.sum(Fee.value))
                            .filter(Fee.check == saved)
                            .one()[0])
        return result if result else 0

    def fees_checked(self) -> int:
        with session_reading() as session:
            result = (session.query(Fee)
                            .filter(Fee.check)
                            .count())
        return result

    def fees_not_checked(self) -> int:
        with session_reading() as session:
            result = (session.query(Fee)
                            .filter(Fee.check == False)
                            .count())
        return result
