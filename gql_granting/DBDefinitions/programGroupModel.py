import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .Base import BaseModel, UUIDFKey, UUIDColumn

class ProgramGroupModel(BaseModel):
    __tablename__ = "acprogramgroups"
    id = UUIDColumn()
    ac_id = (
        UUIDColumn()
    )  # can be a program, also can be a subject, this row can be in a table only once per program and once per subject
    group_id = UUIDFKey()#Column(ForeignKey("groups.id"))