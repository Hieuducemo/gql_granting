import sqlalchemy
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, DECIMAL
from .Base import BaseModel, UUIDFKey, UUIDColumn

class ProgramTypeModel(BaseModel):
    """It encapsulates a study at university, like Cyber defence.

    Args:
        id (ID): An primary key.
        name (str): aka Matematika
        name_en (str): aka Mathematics
        form_id (ID): defines a form (distant, present)
        language_id (ID): defines a language (Czech, English)
        level_id (ID): defines a level (Bacelor, Master, Doctoral, ... )
        title_id (ID): defined a title (Bc., MSc., Ph.D., ...)
    """
    __tablename__ = "acprogramtypes"
    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    form_id = Column(ForeignKey("acprogramforms.id"), index=True)
    language_id = Column(ForeignKey("acprogramlanguages.id"), index=True)
    level_id = Column(ForeignKey("acprogramlevels.id"), index=True)
    title_id = Column(ForeignKey("acprogramtitles.id"), index=True)
    # combination