import datetime

from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.dialects.mysql import LONGTEXT

from src.core.databases.database import Base


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    create = Column(DateTime, nullable=False, default=datetime.datetime.now())
    content = Column(LONGTEXT, nullable=True)
