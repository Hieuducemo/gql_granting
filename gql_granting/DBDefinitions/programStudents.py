import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .Base import BaseModel, UUIDFKey, UUIDColumn

class ProgramStudents(BaseModel):
    __tablename__ = "acprograms_students"
    id = UUIDColumn()
    
    program_id = Column(ForeignKey("acprograms.id"))
    student_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    state_id = Column(ForeignKey("acprograms_studentstates.id"), index=True)
    semester = Column(Integer)

    valid = Column(Boolean, default=lambda item: True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
