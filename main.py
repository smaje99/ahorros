import facade as fd

def main():
    while True:
        x = input('''Sistema de Ahorro
        1. Crear base de datos
        2. Estadísticas
        0. Salir
> ''')
        if x == '1':
            if not fd.exists_db():
                print('Cargando base de datos...')
                fd.load_db()
                print('La base de datos ha sido creada y cargada')
            else:
                print('La base de datos ya ha sido creada con anterioridad')
        elif x == '2':
            print(fd.money_statistics(), end='\n' * 2)
            print(fd.fees_statistics())
        elif x == '0':
            print('Cerrando aplicación...')
            break
        else:
            print('Opción desconocida')


if __name__ == '__main__':
    main()
