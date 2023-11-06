import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from uoishelpers.uuid import UUIDColumn
from .Base import BaseModel, UUIDFKey


class ClassificationLevelModel(BaseModel):
    """Holds a particular classification level (A, B, C, ...).

    Args:
        id (ID): An primary key.
        name (ID): A, B, C, ...
        name_en (ID): A, B, C, ...
        ordervalue = 1, 2, 3, ...
    """
    __tablename__ = "acclassificationlevels"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    ordervalue = Column(Integer)


##############################################