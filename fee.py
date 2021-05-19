from sqlalchemy import Column, Integer, Boolean, String

from base import Base


class Fee(Base):
    '''Representación de la tabla fee
    en la base de datos ahorros
    '''
    __tablename__ ='fee'

    id = Column(Integer,
                primary_key=True,
                unique=True,
                nullable=False,
                autoincrement=True)
    value = Column(Integer, unique=True, nullable=False)
    check = Column(Boolean, nullable=False, default=False)
    figure = Column(String(1), nullable=True)
