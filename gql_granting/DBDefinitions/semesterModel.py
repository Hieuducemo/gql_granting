import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .Base import BaseModel, UUIDFKey, UUIDColumn

class SemesterModel(BaseModel):
    """Aka Mathematics, 2nd semester"""

    __tablename__ = "acsemesters"
    id = UUIDColumn()
    order = Column(Integer)
    credits = Column(Integer)
    subject_id = Column(ForeignKey("acsubjects.id"), index=True)
    classificationtype_id = Column(ForeignKey("acclassificationtypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    # subject = relationship('SubjectModel', back_populates='semesters')
    # classifications = relationship('ClassificationModel', back_populates='classificationsemesters')
    # themes = relationship('StudyThemesModel', back_populates='studysemesters')


##############################################