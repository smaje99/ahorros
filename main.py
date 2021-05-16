from typing import Iterator

from common import config, set_config
from fee import Fee
from database import DataBase

db = DataBase()


def get_fee_values() -> Iterator[Fee]:
    for value in range(50, 10_050, 50):
        yield Fee(value=value)


def load_db():
    for fee in get_fee_values():
        db.add_fee(fee)
    set_config(True)


def main():
    while True:
        x = input('''Sistema de Ahorro
        1. Crear base de datos
        2. Estadísticas
        0. Salir
> ''')
        if x == '1':
            if not config()['exists_db']:
                print('Cargando base de datos...')
                load_db()
                print('La base de datos ha sido creada y cargada')
            else:
                print('La base de datos ya ha sido creada con anterioridad')
        elif x == '2':
            pass
        elif x == '0':
            print('Cerrando aplicación...')
            break
        else:
            print('Opción desconocida')


if __name__ == '__main__':
    main()
