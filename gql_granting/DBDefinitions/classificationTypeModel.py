import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .Base import BaseModel, UUIDFKey, UUIDColumn
from sqlalchemy.orm import relationship 

class ClassificationTypeModel(BaseModel):
    __tablename__ = "acclassificationtypes"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    # Z, KZ, Z+Zk, Zk, ...
    # classificationsemesters = relationship('SemesterModel', back_populates='classifications')
    user_id = UUIDFKey(nullable=True)
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    # classifications = relationship("classificationModel",back_populates="type", uselist= True)