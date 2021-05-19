from colorama import init, Fore

import facade as fd


init(autoreset=True)


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
                print(Fore.GREEN + 'La base de datos ha sido creada y cargada', end='\n' * 2)
            else:
                print(Fore.RED + 'La base de datos ya ha sido creada con anterioridad', end='\n' * 2)
        elif x == '2':
            print(fd.money_statistics(), end='\n' * 2)
            print(fd.fees_statistics(), end='\n' * 2)
        elif x == '3':
            while True:
                x = input('1. Ver tabla\n' + \
                    '2. Registrar cuota\n' + \
                    '3. Eliminar cuota\n' + \
                    '0. Salir\n' + \
                    '> ')
                if x == '1':
                    print(fd.savings_table(), end='\n' * 2)
                elif x == '2':
                    id = int(input('Id de la cuota: '))
                    if not fd.check_fee(id):
                        if fd.has_figure(id):
                            x = input('Esta cuota tiene una bandera ' + \
                                '¿Está seguro de registrarla? (s/n): ') \
                                    .strip() \
                                    .lower()
                            if x == 'n' or x != 's':
                                continue
                        fd.register_fee(id, True)
                        print(Fore.GREEN + 'Cuota registrada exitosamente', end='\n' * 2)
                    else:
                        print(Fore.RED + 'La cuota ya está registrada', end='\n' * 2)
                elif x == '3':
                    id = int(input('Id de la cuota: '))
                    if fd.check_fee(id):
                        if fd.has_figure(id):
                            x = input('Esta cuota tiene una bandera ' + \
                                '¿Está seguro de eliminarla? (s/n): ') \
                                    .strip() \
                                    .lower()
                            if x == 'n' or x != 's':
                                print()
                                continue
                        fd.register_fee(id, False)
                        print(Fore.GREEN + 'Cuota eliminada exitosamente', end='\n' * 2)
                    else:
                        print(Fore.RED + 'La cuota no está registrada', end='\n' * 2)
                elif x == '0':
                    print('Saliendo del registro de cuotas', end='\n' * 2)
                    break
                else:
                    print(Fore.RED + 'Opción desconocida', end='\n' * 2)
        elif x == '0':
            print('Cerrando aplicación...')
            break
        else:
            print(Fore.RED + 'Opción desconocida', end='\n' * 2)


if __name__ == '__main__':
    main()
