from sqlalchemy import Column, Integer, String, Date, Text
from database import Base

class Diary(Base):
    __tablename__ = "diary"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    content = Column(Text)
    summary = Column(String(255))  
    sentiment = Column(String(16)) 
    recommended_projects = Column(Text)  # JSON 문자열로 저장

class BookClubEntry(Base):
    __tablename__ = "bookclub_entry"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    book_title = Column(String(255))
    review = Column(Text)
    summary = Column(String(255))  # 한줄소감
    recommended_projects = Column(Text)  # JSON 문자열로 저장 