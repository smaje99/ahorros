import yaml


__config = None


def config():
    global __config
    if not __config:
        with open('config.yaml', mode='r') as stream:
            __config = yaml.safe_load(stream)
    return __config


def config(exists_db: bool):
    global __config
    __config = None
    with open('config.yaml', mode='w') as stream:
        yaml.dump({'exists_db': exists_db}, stream)
