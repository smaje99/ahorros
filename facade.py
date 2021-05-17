from typing import Iterator

from prettytable import PrettyTable

from common import config, set_config
from fee import Fee
from database import DataBase


db = DataBase()

dollar_millon = lambda value: f'$ {value:6,.0f}'.replace(',', '.')

dollar_thousand = lambda value: f'$ {value:5,.0f}'.replace(',', '.')


def _get_fee_values() -> Iterator[Fee]:
    for value in range(50, 10_050, 50):
        yield Fee(value=value)


def load_db():
    for fee in _get_fee_values():
        db.add_fee(fee)
    set_config(True)


def exists_db() -> bool:
    return config()['exists_db']


def money_statistics() -> str:
    money = PrettyTable(['Ahorrado', 'Faltante'])
    money.add_row([dollar_millon(db.saved_money()),
                   dollar_millon(db.missing_money())])
    return money.get_string(title='Dinero')


def fees_statistics() -> str:
    fees = PrettyTable(['Pagadas', 'Faltantes'])
    fees.add_row([db.fees_checked(), db.fees_not_checked()])
    return fees.get_string(title='Cuotas')
