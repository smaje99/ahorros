from typing import List

from sqlalchemy.sql import func

from base import Base, engine, session_reading, session_writing
from fee import Fee


class DataBase:
    '''Gestión de la creación y conexiones de la base de datos'''

    def __init__(self):
        '''Gestión de la creación y conexiones de la base de datos'''
        Base.metadata.create_all(engine)

    def add_fee(self, fee: Fee):
        '''Añade una cuota a la base de datos

        Args:
            fee (Fee): cuota a añadir a la base de datos
        '''
        with session_writing() as session:
            session.add(fee)

    def get_fee(self, id: int) -> Fee:
        '''Obtiene una cuota en especifico de la base de datos

        Args:
            id (int): identificación de la cuotas

        Returns:
            Fee: Cuota en especifica de la base de datos
        '''
        with session_reading() as session:
            result = (session.query(Fee)
                        .filter(Fee.id == id)
                        .first())
        return result

    def get_fees(self) -> List[Fee]:
        '''Obtiene todas las cuotas de la base de datos

        Returns:
            List[Fee]: lista de todas las cuotas
        '''
        with session_reading() as session:
            result = session.query(Fee).all()
        return result

    def update_fee_check(self, id: int, check: bool):
        '''Actualiza la propiedad :check:`check <fee.Fee.check>`
        en la base datos

        Args:
            id (int): Cuota a actualizar
            check (bool): True: cuota pagada | False: cuota no pagada
        '''
        with session_writing() as session:
            (session.query(Fee)
                .filter(Fee.id == id)
                .update({Fee.check: check}))

    def money(self, saved: bool) -> int:
        '''Sumatoria del dinero ahorrado o faltante de las
        cuotas registradas en la base de datos

        Args:
            saved (bool): True: dinero ahorrado | False: dinero faltante

        Returns:
            int: sumatoria del dinero según lo indicado
        '''
        with session_reading() as session:
            result = (session.query(func.sum(Fee.value))
                            .filter(Fee.check == saved)
                            .one()[0])
        return result if result else 0

    def fees_checked(self, check: bool) -> int:
        '''Cantidad de cuotas pagadas o faltantes
        registradas en la base de datos

        Args:
            check (bool): True: cuotas pagadas | False: cuotas faltantes

        Returns:
            int: cantidad de las cuotas correspondiente
        '''
        with session_reading() as session:
            result = (session.query(Fee)
                            .filter(Fee.check == check)
                            .count())
        return result

    def fees_with_figure(self, figure: str) -> List[Fee]:
        '''Listado de cuotas que comparten
        una bandera en especifica

        Args:
            figure (str): bandera

        Returns:
            List[Fee]: listado de las cuotas
        '''
        with session_reading() as session:
            result = (session.query(Fee)
                            .filter(Fee.figure == figure)
                            .all())
        return result

    def delete_fees(self):
        '''Remueve todos los registros de la cuotas pagadas
        '''
        with session_writing() as session:
            (session.query(Fee)
                .delete(synchronize_session=False))
