from sqlalchemy import Column, Integer, Boolean

from base import Base


class Fee(Base):
    __tablename__ ='fee'

    id = Column(Integer,
                primary_key=True,
                unique=True,
                nullable=False,
                autoincrement=True)
    value = Column(Integer, unique=True, nullable=False)
    check = Column(Boolean, nullable=False, default=False)
