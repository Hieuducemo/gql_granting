import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .Base import BaseModel, UUIDFKey, UUIDColumn
from sqlalchemy.orm import relationship 
class LessonTypeModel(BaseModel):
    __tablename__ = "aclessontypes"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    abbr = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    # lectures, excersise, laboratory, ...

    # items = relationship('StudyThemeItemModel', back_populates='type')

    lessons = relationship("lessonModel", back_populates = "type", uselist = True )
##############################################
