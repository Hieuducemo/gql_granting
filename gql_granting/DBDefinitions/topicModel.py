import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from uoishelpers.uuid import UUIDColumn
from .Base import BaseModel, UUIDFKey
class TopicModel(BaseModel):
    """Aka Functions"""

    __tablename__ = "actopics"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    order = Column(Integer)

    semester_id = Column(ForeignKey("acsemesters.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
