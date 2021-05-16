from typing import List

from base import Base, engine, Session
from fee import Fee


class DataBase:
    def __init__(self):
        Base.metadata.create_all(engine)

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
