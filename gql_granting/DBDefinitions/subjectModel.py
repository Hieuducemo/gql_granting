import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .Base import BaseModel, UUIDFKey, UUIDColumn

class SubjectModel(BaseModel):
    """Could be a Mathematics.

    Args:
        id (ID): An primary key.
        name (str): aka Matematika
        name_en (str): aka Mathematics
        program_id (ID): the program to which subject belongs
    """
    __tablename__ = "acsubjects"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    program_id = Column(ForeignKey("acprograms.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    # language_id = Column(ForeignKey('plan_subject_languages.id'))
    # program = relationship('StudyProgramModel', back_populates='subjects')
    # semesters = relationship('SemesterModel', back_populates='subject')
    # language = relationship('StudyLanguageModel', back_populates='subjects')
