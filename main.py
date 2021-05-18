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
                x = input('1. Ver tabla\n' + \
                    '2. Registrar cuota\n' + \
                    '3. Eliminar cuota\n' + \
                    '0. Salir\n' + \
                    '>')
                if x == '1':
                    print(fd.savings_table(), end='\n' * 2)
                elif x == '2':
                    id = int(input('Id de la cuota: '))
                    if not fd.check_fee(id):
                        if fd.has_figure(id):
                            x = input('Esta cuota tiene una bandera ' + \
                                '¿Está seguro de registrarla? (s/n): ') \
                                    .trim() \
                                    .lower()
                            if x == 'n' or x != 's':
                                continue
                        fd.register_fee(id, True)
                        print('Cuota registrada exitosamente', end='\n' * 2)
                    else:
                        print('Es cuota ya está registrada', end='\n' * 2)
                elif x == '3':
                    id = int(input('Id de la cuota: '))
                    if fd.check_fee(id):
                        if fd.has_figure(id):
                            x = input('Esta cuota tiene una bandera ' + \
                                '¿Está seguro de eliminarla? (s/n): ') \
                                    .trim() \
                                    .lower()
                            if x == 'n' or x != 's':
                                continue
                        fd.register_fee(id, False)
                        print('Cuota eliminada exitosamente', end='\n' * 2)
                    else:
                        print('Es cuota no está registrada', end='\n' * 2)
                elif x == '0':
                    print('Saliendo del registro de cuotas', end='\n' * 2)
                    break
                else:
                    print('Opción desconocida')
        elif x == '0':
            print('Cerrando aplicación...')
            break
        else:
            print('Opción desconocida')


if __name__ == '__main__':
    main()
