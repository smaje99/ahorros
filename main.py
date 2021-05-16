import common
from fee import Fee
from database import Database

db = Database()


def main():
    while True:
        x = input('''Sistema de Ahorro
          1. Crear base de datos
          2. Estadísticas
          0. Salir''')
        if x == '1':
            pass
        elif x == '2':
            pass
        elif x == '0':
            print('Cerrando aplicación...')
            break
        else:
            print('Opción desconocida')


if __name__ == '__main__':
    main()
