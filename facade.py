from typing import Iterator
from itertools import zip_longest

from prettytable import PrettyTable
from colorama import Fore, init

from common import config, set_config
from fee import Fee
from database import DataBase


db = DataBase()

init(autoreset=True)

dollar = lambda value: f'$ {value:6,.0f}'.replace(',', '.')


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
    money.add_row([dollar(db.saved_money()),
                   dollar(db.missing_money())])
    return money.get_string(title='Dinero')


def fees_statistics() -> str:
    fees = PrettyTable(['Pagadas', 'Faltantes'])
    fees.add_row([db.fees_checked(), db.fees_not_checked()])
    return fees.get_string(title='Cuotas')


def savings_table() -> str:
    table = PrettyTable(['Lunes',
                         'Martes',
                         'Miércoles',
                         'Jueves',
                         'Viernes',
                         'Sábado',
                         'Domingo'])
    color = lambda check: Fore.GREEN if check else Fore.RED
    values = map(
        lambda fee: f'{color(fee.check)} {fee.id:3}: {dollar(fee.value)}',
        db.get_fees()
    )

    for week in zip_longest(*[iter(values)]*7, fillvalue='     $     -'):
        table.add_row(week)
    return table.get_string(title='Tabla de Ahorros')
