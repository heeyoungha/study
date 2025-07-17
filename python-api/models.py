from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Diary(Base):
    __tablename__ = "diary"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    sentiment = Column(String(16), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    recommended_projects = Column(Text, nullable=True)  # JSON 문자열로 저장 