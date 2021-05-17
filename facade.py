from typing import Iterator

from common import config, set_config
from fee import Fee
from database import DataBase


db = DataBase()


def _get_fee_values() -> Iterator[Fee]:
    for value in range(50, 10_050, 50):
        yield Fee(value=value)


def load_db():
    for fee in _get_fee_values():
        db.add_fee(fee)
    set_config(True)


def exists_db() -> bool:
    return config()['exists_db']
