import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from uoishelpers.uuid import UUIDColumn
from .Base import BaseModel, UUIDFKey


class ProgramStudentMessages(BaseModel):
    __tablename__ = "acprograms_studentmessages"
    id = UUIDColumn()
    name = Column(String)
    description = Column(String)
    student_id = Column(ForeignKey("acprograms_students.id"), index=True)
    program_id = Column(ForeignKey("acprograms.id"), index=True)
    date = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)