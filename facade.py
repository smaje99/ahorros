from typing import Iterator
from itertools import zip_longest

from prettytable import PrettyTable
from colorama import Fore

from common import config, set_config
from fee import Fee
from database import DataBase


db = DataBase()

# Formateo dólar a un número
dollar = lambda value: f'$ {value:6,.0f}'.replace(',', '.')


def _get_fee_values() -> Iterator[Fee]:
    '''Genera los valores de las cuotas
    para la base de datos

    Yields:
        Iterator[Fee]: valores de las cuotas
    '''
    for value in range(50, 10_050, 50):
        yield Fee(value=value)


def _add_figure(fee: Fee):
    '''Añade una bandera a la cuota
    según su valor

    Args:
        fee (Fee): cuota a añadir la bandera
    '''
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
    '''Carga las cuotas en la base de datos
    y configura la creación de la misma
    '''
    for fee in _get_fee_values():
        _add_figure(fee)
        db.add_fee(fee)
    set_config(True)


def remove_db():
    '''Remueve la base de datos actual
    '''
    db.delete_fees()
    set_config(False)


def exists_db() -> bool:
    '''Confirma la existencia de la base de datos

    Returns:
        bool: existencia de la base de datos
    '''
    return config()['exists_db']


def money_statistics() -> str:
    '''Estadísticas del dinero existente

    Returns:
        str: tabla de comparación del dinero ahorrado y faltante
    '''
    money = PrettyTable(['Ahorrado', 'Faltante'])
    money.add_row([dollar(db.money(True)),
                   dollar(db.money(False))])
    return money.get_string(title='Dinero')


def fees_statistics() -> str:
    '''Estadísticas de las cuotas existentes

    Returns:
        str: tabla de comparación de las cuotas ahorradas y faltantes
    '''
    fees = PrettyTable(['Pagadas', 'Faltantes'])
    fees.add_row([db.fees_checked(True),
                  db.fees_checked(False)])
    return fees.get_string(title='Cuotas')


def savings_table() -> str:
    '''Tabla de las cuotas en la base de datos
    con su identificación y comprobación de pago

    Returns:
        str: tabla de cuotas
    '''
    table = PrettyTable(['Lunes',
                         'Martes',
                         'Miércoles',
                         'Jueves',
                         'Viernes',
                         'Sábado',
                         'Domingo'])
    color = lambda check: Fore.GREEN if check else Fore.RED
    values = map(
        lambda fee: f'{color(fee.check)} {fee.id:3}: {dollar(fee.value)}{Fore.RESET}',
        db.get_fees()
    )
    for week in zip_longest(*[iter(values)]*7, fillvalue='     $     -'):
        table.add_row(week)
    return table.get_string(title='Tabla de Ahorros')


def check_fee(id: int) -> bool:
    '''Comprueba si una cuota está pagada
    o en estado faltante

    Args:
        id (int): cuota a comprobar

    Returns:
        bool: estado de la cuota
    '''
    return db.get_fee(id).check


def register_fee(id: int, check: bool):
    '''Registra el pago o el despago de una cuota est

    Args:
        id (int): cuota a registrar
        check (bool): estado a registrar de la cuota
    '''
    db.update_fee_check(id, check)


def has_figure(id: int) -> bool:
    '''Comprueba si una cuota tiene una bandera

    Args:
        id (int): cuota a comprobar

    Returns:
        bool: comprobación de bandera
    '''
    return bool(db.get_fee(id).figure)


def pay_figure(figure: str) -> int:
    '''Pagar cuotas especificas con una
    determinada bandera

    Args:
        figure (str): bandera

    Returns:
        int: resto del pago
    '''
    rest = 0
    for fee in db.fees_with_figure(figure):
        if fee.check: rest += fee.value
        else: db.update_fee_check(fee.id, True)
    return rest
