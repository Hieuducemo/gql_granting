import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from uoishelpers.uuid import UUIDColumn
from .Base import BaseModel, UUIDFKey

class ProgramTitleTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence.

    Args:
        id (ID): An primary key.
        name (str): aka Bc.
        name_en (str): aka Bc.
    """
    __tablename__ = "acprogramtitles"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    # Bc., Mgr., Ing, ...

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
