import facade as fd

def main():
    while True:
        x = input('''Sistema de Ahorro
        1. Crear base de datos
        2. Estadísticas
        3. Registrar cuotas
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
        elif x == '3':
            while True:
                x = input('1. Ver tabla' + \
                    '2. Registrar cuota' + \
                    '3. Eliminar cuota' + \
                    '0. Salir' + \
                    '>')
                if x == '1':
                    pass
                elif x == '2':
                    pass
                elif x == '3':
                    pass
                elif x == '0':
                    print('Saliendo del registro de cuotas', end='\n' * 2)
                else:
                    print('Opción desconocida')
        elif x == '0':
            print('Cerrando aplicación...')
            break
        else:
            print('Opción desconocida')


if __name__ == '__main__':
    main()
