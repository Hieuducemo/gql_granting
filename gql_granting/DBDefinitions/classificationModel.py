import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .Base import BaseModel, UUIDFKey, UUIDColumn
from sqlalchemy.orm import relationship 

class ClassificationModel(BaseModel):
    """Holds a particular classification for a student.

    Args:
        id (ID): An primary key.
        order (int): 1 for first attempt.
        classificationtype_id (ID): Exam or so
        classificationlevel_id = A, B, C, ...
    """
    __tablename__ = "acclassifications"

    id = UUIDColumn()
    order = Column(Integer) #

    semester_id = Column(ForeignKey("acsemesters.id"), index=True)
    user_id = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True)
    classificationtype_id = Column(ForeignKey("acclassificationtypes.id"), index=True)
    classificationlevel_id = Column(ForeignKey("acclassificationlevels.id"), index=True)

    date = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    type = relationship("classificationTypeModel",back_populates="classifications",uselist = True)