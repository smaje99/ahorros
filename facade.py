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

values_figure = {'c': 20_000,
                 'r': 40_000,
                 'm': 60_000,
                 's': 80_000,
                 't': 100_000}


def _get_fee_values() -> Iterator[Fee]:
    for value in range(50, 10_050, 50):
        yield Fee(value=value)


def _add_figure(fee: Fee):
    figures = {'c': [250, 500, 850, 1150, 1450, 1750, 2050, 2250, 2650, 3150, 3950],
               'r': [50, 300, 1600, 1950, 2350, 2550, 2850, 3300, 3450, 3750, 4050, 4250, 4650, 4900],
               'm': [950, 1550, 3000, 3550, 4350, 5150, 5450, 5650, 5750, 5950, 6050, 6250, 6350],
               's': [350, 1350, 1850, 2150, 3650, 3850, 4450, 5350, 5550, 5850, 6550, 6850, 7150, 7950, 8350, 8750],
               't': [150, 750, 1250, 1650, 2750, 2950, 4150, 4550, 4750, 7350, 7450, 7650, 8250, 8550, 8850, 9350, 9650, 9950]}
    for key, value in figures.items():
        if fee.value in value:
            fee.figure = key
            break


def load_db():
    for fee in _get_fee_values():
        _add_figure(fee)
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


def check_fee(id: int) -> bool:
    return db.get_fee(id).check


def register_fee(id: int, check: bool):
    db.update_fee_check(id, check)
