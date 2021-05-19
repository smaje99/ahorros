import yaml


__config = None


def config():
    '''Lectura del archivo YAML config

    Returns:
        dict: propiedades de configuración
    '''
    global __config
    if not __config:
        with open('config.yaml', mode='r') as stream:
            __config = yaml.safe_load(stream)
    return __config


def set_config(exists_db: bool):
    '''Modificación de la propiedad exists_db
    del archivo de configuración

    Args:
        exists_db (bool): valor de la propiedad
    '''
    global __config
    __config = None
    with open('config.yaml', mode='w') as stream:
        yaml.dump({'exists_db': exists_db}, stream)
