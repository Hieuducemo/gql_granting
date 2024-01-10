import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .Base import BaseModel, UUIDFKey, UUIDColumn
from sqlalchemy.orm import relationship 
class LessonModel(BaseModel):
    """Lecture, 2h,"""

    __tablename__ = "aclessons"
    id = UUIDColumn()
    topic_id = Column(ForeignKey("actopics.id"), index=True)
    type_id = Column(ForeignKey("aclessontypes.id"), index=True)
    count = Column(Integer)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

    type = relationship('LessonTypeModel', back_populates='lessons', uselist = True)
    # theme = relationship('StudyThemeModel', back_populates='items')
